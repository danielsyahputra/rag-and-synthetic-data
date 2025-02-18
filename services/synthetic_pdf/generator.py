import json
import re

from docx import Document
from docx2pdf import convert
from docx.shared import Inches, Mm
from docxtpl import DocxTemplate, InlineImage

from .wrapper import OpenAIWrapper


class BookGenerator:
    def __init__(self) -> None:
        self.wrapper = OpenAIWrapper()

    def generate_title(self, topic, target_audience):
        convo_id = self.wrapper.start_convo(
            system="You are a book author with 20+ experience."
        )
        title_prompt = (
            f'We are writing an eBook. It is about "{topic}". Our'
            f' reader is:  "{target_audience}". Write a short, catch'
            " title clearly directed at our reader that is less than"
            " 9 words and proposes a “big promise” that will be sure to grab"
            " the readers attention."
        )
        title = self.wrapper.msg_in_convo(convo_id, title_prompt)
        title = title.replace('"', "")
        return title

    def verify_outline(self, outline, num_chapters, num_subsections):
        if len(outline.items()) != num_chapters:
            return False
        for chapter, subtopics in outline.items():
            if len(chapter) < 15:
                return False
            if type(subtopics) != list:
                return False
            if len(subtopics) != num_subsections:
                return False
        return True

    def generate_outline(
        self, topic, target_audience, title, num_chapters, num_subsections
    ):
        convo_id = self.wrapper.start_convo(
            "You are a book author with 20+ experience."
        )
        outline_prompt = (
            f'We are writing an eBook called "{title}". It is about'
            f' "{topic}". Our reader is:  "{target_audience}".  Create'
            " a compehensive outline for our ebook, which will have"
            f" {num_chapters} chapter(s). Each chapter should have exactly"
            f" {num_subsections} subsection(s) Output Format for prompt:"
            " python dict with key: chapter title, value: a single list/array"
            " containing subsection titles within the chapter (the subtopics"
            " should be inside the list). The chapter titles should be"
            ' prepended with the chapter number, like this: "Chapter 5:'
            ' [chapter title]". The subsection titles should be prepended'
            ' with the {chapter number.subtitle number}, like this: "5.4:'
            ' [subsection title]". '
        )
        outline_json = self.wrapper.msg_in_convo(convo_id, outline_prompt)
        outline_json = outline_json[
            outline_json.find("{") : outline_json.rfind("}") + 1
        ]
        outline = json.loads(outline_json)
        if not self.verify_outline(outline, num_chapters, num_subsections):
            raise Exception("Outline not well formed!")
        return outline

    def generate_chapter_content(
        self, title, topic, target_audience, idx, chapter, subtopic
    ):
        convo_id = self.wrapper.start_convo(
            "You are a book author with 20+ experience."
        )
        num_words_str = "500 to 700"
        content_prompt = (
            f'We are writing an eBook called "{title}". Overall, it is about'
            f' "{topic}". Our reader is:  "{target_audience}". We are'
            f" currently writing the #{idx+1} section for the chapter:"
            f' "{chapter}". Using at least {num_words_str} words, write the'
            " full contents of the section regarding this subtopic:"
            f' "{subtopic}". The output should be as helpful to the reader as'
            " possible. Include quantitative facts and statistics, with"
            " references. Go as in depth as necessary. You can split this"
            " into multiple paragraphs if you see fit. The output should also"
            ' be in cohesive paragraph form. Do not include any "[Insert'
            ' ___]" parts that will require manual editing in the book later.'
            " If find yourself needing to put 'insert [blank]' anywhere, do"
            " not do it (this is very important). If you do not know"
            " something, do not include it in the output. Exclude any"
            " auxillary information like  the word count, as the entire"
            " output will go directly into the ebook for readers, without any"
            " human procesing. Remember the {num_words_str} word minimum,"
            " please adhere to it."
        )
        content = self.wrapper.msg_in_convo(convo_id, content_prompt)

        def remove_subtopic_from_content(content, subtopic, search_limit=200):
            pattern = r"\d\.\d"

            match = re.search(pattern, content[:search_limit])

            if match:
                newline_index = content.find("\n", match.end())

                if newline_index != -1:
                    result_string = content[newline_index + 1 :]
                    content = content.strip()
                    return result_string
            return content

        try:
            content = content.strip()
            content = remove_subtopic_from_content(content, subtopic)
        except:
            pass
        return content

    def generate_docs(
        self,
        topic,
        target_audience,
        title,
        outline,
        docx_file,
        book_template,
        preview,
        actionable_steps=False,
    ):
        document = Document(book_template)
        document.add_page_break()
        document.add_heading("Table of Contents")

        for chapter, subtopics in outline.items():
            document.add_heading(chapter, level=2)
            for idx, subtopic in enumerate(subtopics):
                document.add_heading("\t" + subtopic, level=3)

        document.add_page_break()
        chapter_num = 1

        for chapter, subtopic in outline.items():
            document.add_heading(chapter, level=1)
            subtopics_content = []
            for idx, subtopic in enumerate(subtopics):
                if preview and idx >= 2:
                    break
                document.add_heading(subtopic, level=2)
                content = self.generate_chapter_content(
                    title, topic, target_audience, idx, chapter, subtopic
                )
                document.add_paragraph(content)
                subtopics_content.append(content)

            if preview:
                document.add_heading(
                    "Preview Completed - Purchase Full Book To Read More!"
                )
                break

            if chapter_num < len(outline.items()):
                document.add_page_break()
            chapter_num += 1
        document.save(docx_file)

    def generate_cover(
        self, cover_template, title, topic, target_audience, output_file, preview
    ):
        temp_docx = "tmp/temp_cover_intermediate.docx"
        temp_photo = "tmp/preview_photo.png"

        output_pdf = output_file.rsplit(".", 1)[0] + ".pdf"

        doc = DocxTemplate(cover_template)

        if preview:
            image_path = preview
        else:
            self.generate_cover_photo(title, topic, target_audience, temp_photo)
            image_path = temp_photo

        try:
            imagen = InlineImage(doc, image_path, width=Mm(120))
            context = {"title": title, "subtext": "DNL Publishing", "image": imagen}
            doc.render(context)

            doc.save(temp_docx)

            convert(temp_docx, output_pdf)

        finally:
            import os

            try:
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
                if os.path.exists(temp_photo) and not preview:
                    os.remove(temp_photo)
            except Exception as e:
                print(f"Warning: Could not clean up temporary files: {e}")

    def generate_cover_photo(self, title, topic, target_audience, img_output):
        convo_id = self.wrapper.start_convo(
            "You are a book author with 20+ experience."
        )
        cover_prompt = (
            f'We have a ebook with the title {title}. It is about "{topic}".'
            f' Our reader is:  "{target_audience}". Write me a very brief and'
            " matter-of-fact description of a photo that would be on the"
            " cover of the book. Do not reference the cover or photo in your"
            ' answer. For example, if the title was "How to lose weight for'
            ' middle aged women", a reasonable response would be "a middle'
            ' age woman exercising"'
        )
        print(cover_prompt)
        dalle_prompt = self.wrapper.msg_in_convo(convo_id, cover_prompt)
        print(dalle_prompt)

        img_data = self.wrapper.generate_photo(dalle_prompt)
        with open(img_output, "wb") as handler:
            handler.write(img_data)


if __name__ == "__main__":
    generator = BookGenerator()
    topic = "impact of generative ai in industry"
    title = generator.generate_title(topic=topic, target_audience="enterprise")
    print("Title: ", title)
    target_audience = "c-level and high level manager"
    num_chapters = 2
    num_subsections = 5
    outline = generator.generate_outline(
        topic=topic,
        target_audience=target_audience,
        title=title,
        num_chapters=num_chapters,
        num_subsections=num_subsections,
    )
    sample_chapter, sample_subtopics = list(outline.items())[0]
    print("Outline: ", outline)
    subtopic = sample_subtopics[0]
    content = generator.generate_chapter_content(
        title=title,
        topic=topic,
        target_audience=target_audience,
        idx=0,
        chapter=sample_chapter,
        subtopic=subtopic,
    )
    # print(content)
    generator.generate_docs(
        topic=topic,
        target_audience=target_audience,
        title=title,
        outline=outline,
        docx_file="tmp/temp.docx",
        book_template=None,
        preview=False,
    )
    generator.generate_cover_photo(
        title=title,
        topic=topic,
        target_audience=target_audience,
        img_output="tmp/image.png",
    )
    generator.generate_cover(
        cover_template="tmp/temp.docx",
        title=title,
        topic=topic,
        target_audience=target_audience,
        output_file="tmp/book.pdf",
        preview="tmp/image.png",
    )


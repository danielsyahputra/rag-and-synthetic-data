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


if __name__ == "__main__":
    generator = BookGenerator()
    title = generator.generate_title(
        topic="impact of generative ai in industry", target_audience="enterprise"
    )
    print(title)

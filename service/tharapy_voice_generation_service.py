import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai._legacy_response import HttpxBinaryResponseContent

from constant import EnvKeys
from repository import TherapyOutlineRepository
from helper import Logger
from openai import OpenAI

load_dotenv()


class TherapyGenerationService:
    def __init__(self):
        self.therapy_outline_repository = TherapyOutlineRepository()
        self.openai = OpenAI(
            api_key=os.getenv(EnvKeys.OPENAI_API_KEY.value),
        )
        self.logger = Logger(__name__)

    def generate_voice_for_therapy_outline(self, therapy_outline_id: str) -> None:
        self.logger.info(f"Generating voice for therapy outline: {therapy_outline_id}")

        # Fetch therapy outline
        therapy_outline = self.therapy_outline_repository.get_therapy_outline_by_id(therapy_outline_id)
        if not therapy_outline:
            raise ValueError(f"No therapy outline found with ID: {therapy_outline_id}")

        # Ensure the audio directory exists
        audio_directory = Path("audio")
        audio_directory.mkdir(parents=True, exist_ok=True)

        # Generate audio for each step
        for step in therapy_outline.steps:
            if not step.script or not step.script.text:
                self.logger.warning(f"No script available for step {step.step}. Skipping.")
                continue

            self.logger.info(f"Generating voice for step {step.step}")
            audio_url = audio_directory / f"{therapy_outline_id}_{step.step}.mp3"
            response = self._generate_voice(step.script.voice, step.script.text)
            response.stream_to_file(audio_url)
            step.audio_url = audio_url.name
            self.logger.info(f"Voice generated for step {step.step}")

        self.logger.info(f"Updating therapy outline with generated audio: {therapy_outline_id}")
        self.therapy_outline_repository.update_therapy_outline_by_id(therapy_outline_id, therapy_outline)

    def _generate_voice(self, voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                        text: str) -> HttpxBinaryResponseContent:
        self.logger.info(f"Generating voice using {voice} for text: {text[:50]}...")

        response = self.openai.audio.speech.create(
            model="tts-1",
            input=text,
            voice="shimmer"
        )

        return response


# if __name__ == '__main__':
#     service = TherapyGenerationService()
#     print(service.generate_voice_for_therapy_outline("67506c4f182bc2cab7cdc3b1"))

from gtts import gTTS
import os

def convert_text_to_speech(text_list):
    # Ensure the output directory exists or create it if it doesn't
    output_directory = "assets/voices"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through the list and convert each text to MP3
    for index, text in enumerate(text_list, start=1):
        # Initialize the gTTS object with the text
        tts = gTTS(text, lang='en')

        file_name = f"audio_{index}.mp3"

        # Save the generated MP3 to a file in the specified directory
        file_path = os.path.join(output_directory, file_name)
        tts.save(file_path)

        print(f"Saved: {file_path}")

    print("Conversion complete!\n")

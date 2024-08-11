import os
import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

def create_audio(file_name, text):
    ckpt_base = 'checkpoints/base_speakers/EN'
    ckpt_converter = 'checkpoints/converter'
    device="cuda:0" if torch.cuda.is_available() else "cpu"
    output_dir = 'outputs'

    base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
    base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    os.makedirs(output_dir, exist_ok=True)

    source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to(device)

    reference_speaker = 'resources/example_reference.mp3' # This is the voice you want to clone
    print("going in\n")
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed', vad=True)

    save_path = f'{output_dir}/result.wav'

    # Run the base speaker tts
    src_path = f'{output_dir}/tmp.wav'
    base_speaker_tts.tts(text, src_path, speaker='default', language='English', speed=1.0)

    # Run the tone color converter
    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path=src_path, 
        src_se=source_se, 
        tgt_se=target_se, 
        output_path=save_path,
        message=encode_message)
    return save_path
    

if __name__ == "__main__":
    file_name = input("Enter the File Name in Resources: ")
    text = input("Enter the text: ")

    print("The file is saved in ", create_audio(file_name,text))
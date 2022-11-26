import os.path
import argparse
from processing import process_video


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# initilaize argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--single_video', type=str2bool, required=True)
parser.add_argument('--url', type=str, required=True)
parser.add_argument('--language', type=str, required=True)
parser.add_argument('--data_path', type=str, required=True)
parser.add_argument('--gen_output_video', type=str2bool, required=False, nargs='?', const=True, default=True)
parser.add_argument('--download_path', type=str, required=True)
parser.add_argument('--translator', type=str, required=True)

args = parser.parse_args()

print(f'single_video: {args.single_video}\nurl: {args.url}\nlanguage: {args.language}\ndata_path: {args.data_path}\ngen_output: {args.gen_output_video}\ndownload_path: {args.download_path}\ntranslator: {args.translator}')

#validate arguments
suppported_languages = {'chinese':'zh-cn', 'spanish':'es'}
supported_translators = ['google','deepl']

assert(True if args.single_video else os.path.exists(args.url))
assert(args.language in suppported_languages.values())
os.makedirs(args.data_path, exist_ok=True)
assert(os.path.exists(args.download_path))
assert(args.translator in supported_translators)


if args.single_video == True:
    process_video(args.language, args.url, args.data_path, args.download_path, args.translator, args.gen_output_video)

else:
    f = open(args.url, 'r')
    urls = f.readlines()
    for i,link in enumerate(urls):
        print(f'processing video {i+1}')
        process_video(args.language, link, args.data_path, args.download_path, args.translator, args.gen_output_video)
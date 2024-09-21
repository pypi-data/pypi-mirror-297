from bioclip import TreeOfLifeClassifier, Rank, CustomLabelsClassifier
from .predict import BIOCLIP_MODEL_STR
import open_clip as oc
import os
import json
import sys
import prettytable as pt
import pandas as pd
import argparse


def write_results(data, format, output):
    df = pd.DataFrame(data)
    if output == 'stdout':
        write_results_to_file(df, format, sys.stdout)
    else:
        with open(output, 'w') as outfile:
            write_results_to_file(df, format, outfile)


def write_results_to_file(df, format, outfile):
    if format == 'table':
        table = pt.PrettyTable()
        table.field_names = df.columns
        for index, row in df.iterrows():
            table.add_row(row)
        outfile.write(str(table))
        outfile.write('\n')
    elif format == 'csv':
        df.to_csv(outfile, index=False)
    else:
        raise ValueError(f"Invalid format: {format}")


def predict(image_file: list[str],
            format: str,
            output: str,
            cls_str: str,
            rank: Rank,
            k: int,
            **kwargs):
    if cls_str:
        classifier = CustomLabelsClassifier(cls_ary=cls_str.split(','), **kwargs)
        predictions = classifier.predict(image_paths=image_file, k=k)
        write_results(predictions, format, output)
    else:
        classifier = TreeOfLifeClassifier(**kwargs)
        predictions = classifier.predict(image_paths=image_file, rank=rank, k=k)
        write_results(predictions, format, output)


def embed(image_file: list[str], output: str, **kwargs):
    classifier = TreeOfLifeClassifier(**kwargs)
    images_dict = {}
    data = {
        "model": classifier.model_str,
        "embeddings": images_dict
    }
    for image_path in image_file:
        features = classifier.create_image_features_for_path(image_path=image_path, normalize=False)
        images_dict[image_path] = features.tolist()
    if output == 'stdout':
        print(json.dumps(data, indent=4))
    else:
        with open(output, 'w') as outfile:
            json.dump(data, outfile, indent=4)


def create_parser():
    parser = argparse.ArgumentParser(prog='bioclip', description='BioCLIP command line interface')
    subparsers = parser.add_subparsers(title='commands', dest='command')

    device_arg = {'default':'cpu', 'help': 'device to use (cpu or cuda or mps), default: cpu'}
    output_arg = {'default': 'stdout', 'help': 'print output to file, default: stdout'}
    model_arg = {'help': f'model identifier (see command list-models); default: {BIOCLIP_MODEL_STR}'}
    pretrained_arg = {'help': 'pretrained model checkpoint as tag or file, depends on model; '
                              'needed only if more than one is available (see command list-models)'}

    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Use BioCLIP to generate predictions for image files.')
    predict_parser.add_argument('image_file', nargs='+', help='input image file(s)')
    predict_parser.add_argument('--format', choices=['table', 'csv'], default='csv', help='format of the output, default: csv')
    predict_parser.add_argument('--output', **output_arg)
    predict_parser.add_argument('--rank', choices=['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'],
                                help='rank of the classification, default: species (when)')
    predict_parser.add_argument('--k', type=int, help='number of top predictions to show, default: 5')
    cls_help = "classes to predict: either a comma separated list or a path to a text file of classes (one per line), when specified the --rank argument is not allowed."
    predict_parser.add_argument('--cls', help=cls_help)

    predict_parser.add_argument('--device', **device_arg)
    predict_parser.add_argument('--model', **model_arg)
    predict_parser.add_argument('--pretrained', **pretrained_arg)

    # Embed command
    embed_parser = subparsers.add_parser('embed', help='Use BioCLIP to generate embeddings for image files.')
    embed_parser.add_argument('image_file', nargs='+', help='input image file(s)')
    embed_parser.add_argument('--output', **output_arg)
    embed_parser.add_argument('--device', **device_arg)
    embed_parser.add_argument('--model', **model_arg)
    embed_parser.add_argument('--pretrained', **pretrained_arg)

    # List command
    list_parser = subparsers.add_parser('list-models',
                                        help='List available models and pretrained model checkpoints.',
                                        description=
                                             'Note that this will only list models known to open_clip; '
                                             'any model identifier loadable by open_clip, such as from hf-hub, file, etc '
                                             'should also be usable for --model in the embed and predict commands. '
                                             f'(The default model {BIOCLIP_MODEL_STR} is one example.)')
    list_parser.add_argument('--model', help='list available tags for pretrained model checkpoint(s) for specified model')

    return parser


def parse_args(input_args=None):
    args = create_parser().parse_args(input_args)
    if args.command == 'predict':
        if args.cls:
            # custom class list mode
            if args.rank:
                raise ValueError("Cannot use --cls with --rank")
        else:
            # tree of life class list mode
            if args.model or args.pretrained:
                raise ValueError("Custom model or checkpoints currently not supported for Tree-of-Life prediction")
            if not args.rank:
                args.rank = 'species'
            args.rank = Rank[args.rank.upper()]
            if not args.k:
                args.k = 5
    return args


def create_classes_str(cls_file_path):
    """Reads a file with one class per line and returns a comma separated string of classes"""
    with open(cls_file_path, 'r') as cls_file:
        cls_str = [item.strip() for item in cls_file.readlines()]
    return ",".join(cls_str)


def main():
    args = parse_args()
    if args.command == 'embed':
        embed(args.image_file,
              args.output,
              device=args.device,
              model_str=args.model,
              pretrained_str=args.pretrained)
    elif args.command == 'predict':
        cls_str = args.cls
        if args.cls and os.path.exists(args.cls):
            cls_str = create_classes_str(args.cls)
        predict(args.image_file,
                format=args.format,
                output=args.output,
                cls_str=cls_str,
                rank=args.rank,
                k=args.k,
                device=args.device,
                model_str=args.model,
                pretrained_str=args.pretrained)
    elif args.command == 'list-models':
        if args.model:
            for tag in oc.list_pretrained_tags_by_model(args.model):
                print(tag)
        else:
            for model_str in oc.list_models():
                print(f"\t{model_str}")
    else:
        raise ValueError("Invalid command")


if __name__ == '__main__':
    main()

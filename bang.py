import sys

import click

from src.linbang import LogisticBang
from src.parser import lines_transformer


def print_header(bit_precision, sigma, quadratic_interactions):
    out = "Num weight bits = {}\n".format(bit_precision)
    sys.stdout.write(out)

    out = "Initial sigma = {}\n".format(sigma)
    sys.stdout.write(out)

    if quadratic_interactions:
        out = "Quadratic interactions = {}\n".format(', '.format(quadratic_interactions))
        sys.stdout.write(out)

    out = "average" + "\t\t" + "example" + "\t\t" + "example" + "\t\t" + "current" + "\t\t" + "current" + "\t\t"
    out += "current" + "\n"
    out += "loss" + "\t\t" + "counter" + "\t\t" + "weight" + "\t\t" + "label" + "\t\t" + "predict" + "\t\t"
    out += "features" + "\n"
    sys.stdout.write(out)


@click.command()
@click.option('-q', '--quadratic', 'quadratic_interactions', default='', multiple=True, type=str)
@click.option('-b', '--bit_precision', 'bit_precision', default=23, type=int)
@click.option('-t', '--testonly/--learn', 'testonly', default=False)
@click.option('-s', '--sigma', 'sigma', default=0.01, type=float)
@click.option('-m', '--mode/--sampling', 'mode', default=True)
@click.option('-f', '--final_regressor', 'final_regressor', default='', type=click.Path(exists=False))
@click.option('-i', '--initial_regressor', 'initial_regressor', default='', type=click.Path(exists=False))
@click.option('-P', '--progress', 'progress', default=100, type=int)
@click.option('--quiet/--no-quiet', 'quiet', default=False)
def bang(quadratic_interactions, bit_precision, testonly, mode, sigma, progress, final_regressor,
         initial_regressor, quiet):
    if not quiet:
        print_header(bit_precision, sigma, quadratic_interactions)

    model = LogisticBang(bit_precision, sigma)
    if initial_regressor:
        model.load(initial_regressor)

    rows = click.get_text_stream('stdin')
    for i, row in enumerate(lines_transformer(rows, quadratic_interactions, bit_precision)):
        if not testonly:
            model.partial_fit(row)
        if mode:
            prediction = model.predict(row)
        else:
            prediction = model.sample_predict(row)

        label, weight, _, features = row
        if not i % progress:
            if quiet:
                out = "%.4f" % prediction + "\n"
                sys.stdout.write(out)
            else:
                out = "%.4f" % model.average_loss + "\t\t" + str(model.example_counter) + "\t\t" + str(weight) + "\t\t"
                out += str(label) + "\t\t" + "%.4f" % prediction + "\t\t" + str(len(features)) + "\n"
                sys.stdout.write(out)

    if final_regressor:
        model.dump(final_regressor)


if __name__ == "__main__":
    bang()

# autobi_py

A Python wrapper and interfacing library around [AuToBI](https://github.com/AndrewRosenberg/AuToBI). AuToBI is effectively the only publically available system for the automatic generation of prosody transcriptions, created by Andrew Rosenberg for his PhD in 2012.

AuToBI_py provides a simple Python interface for AuToBI's feature generation systems, as well as the parts of AuToBI that are available from the command line.

## Usage

To get started, the JVM needs to be running, as the Java code can otherwise not be called. To start the JVM, use the `AutobiJVMHandler` class like so:

```python
from autobi.core import AutobiJVMHandler

with AutobiJVMHandler() as jvm:
    do_stuff(jvm)
```

`AutobiJVMHandler` returns a handle to the JVM (type `autobi.core.AutobiJVM`) that you can pass into functions from this library to let them access it. The constructor can take one argument, a string name, that is used to distinguish separate views of the JVM as follows:

```python
from autobi.core import AutobiJVMHandler

with AutobiJVMHandler("test") as jvm1:
    with AutobiJVMHandler("test") as jvm2:
        assert jvm1 is jvm2

with AutobiJVMHandler("second_test1") as jvm1:
    with AutobiJVMHandler("second_test2") as jvm2:
        assert jvm1 is not jvm2

# The default argument is "main"
with AutobiJVMHandler() as jvm1:
    with AutobiJVMHandler("main") as jvm2:
        assert jvm1 is jvm2
```

If you want to hard shutdown the JVM and invalidate all `AutobiJVM` instances for some reason, run `autobi.core._shutdown()`.

### Running AuToBI like from the commandline

To run AuToBI like you would from the commandline, use the `RunDefault` or `TrainDefault` class:

```python
from autobi import RunDefault
from autobi.core import AutobiJVMHandler

with AutobiJVMHandler() as jvm:
    RunDefault(jvm).run("-input_file=test.TextGrid -wav_file=test.wav ...")

    # One argument has been added to argument list in the adapter
    # "-adapter_test", which prints "TEST SUCCESS: The adapter is running"
    RunDefault(jvm).run("-adapter_test")

# Alternatively, you might want to use the TrainDefault class.
# This is equivilant to calling the AuToBI jar file with the main function
# from the edu.cuny.qc.speech.AuToBI.AuToBITrainer class instead.
from autobi import TrainDefault

with AutobiJVMHandler() as jvm:
    TrainDefault(jvm).run("commandline_arguments")
```

To make creating arguments for running like this easier, there is the `ArgumentBuilder` class, which works for both `RunDefault` and `TrainDefault`:

```python
from pathlib import Path

from autobi import RunDefault, ArgumentBuilder
from autobi.core import AutobiJVMHandler

with AutobiJVMHandler("test") as jvm:
    builder = ArgumentBuilder(jvm)
    builder.with_output_file(Path() / "out.arff")
    builder.with_input_wav(Path() / "test.wav")
    builder.with_input_TextGrid(Path() / "test.TextGrid")
    builder.with_charset("hello")
    args = builder.to_args_string()

    RunDefault(jvm).run(args)
```

### Extracting features

The most important part of the adapter is the ability to use AuToBI's excellent feature extraction algorithms on their own. The majority of Rosenberg's PhD was dedicated to feature extraction, and a large majority of the code is, too.

#### Creating a FeatureSet to extract.

The primary interface for this is the `autobi.FeatureSet` class, which is simply a wrapper around a list of strings, where each string represents a valid feature.

To generate one of these feature sets, use the `FeaturenamesBuilder` class:

```python
from autobi import FeaturenamesBuilder
from autobi.core import AutobiJVMHandler

# With individual features:
with AutobiJVMHandler() as jvm:
    builder = FeaturenamesBuilder(jvm)
    builder.with_feature(r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]")
    builder.with_feature(r"mean[subregionC[znormC[f0],subregion[200ms]]]")
    featureset = builder.build()

# With default feature sets from AuToBi:
with AutobiJVMHandler() as jvm:
    builder = FeaturenamesBuilder(jvm)
    builder.with_default_features("PhraseAccentClassificationFeatureSet")
    featureset = builder.build()

# Of course, these can be combinded:
with AutobiJVMHandler() as jvm:
    builder = FeaturenamesBuilder(jvm)
    builder.with_default_features("PhraseAccentClassificationFeatureSet")
    builder.with_feature(r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]")
    builder.with_feature(r"mean[subregionC[znormC[f0],subregion[200ms]]]")
    featureset = builder.build()
```

What individual features are valid is not documented anywhere for AuToBI. The default feature sets, however, are simply the names of the [Java classes that inherit from FeatureSet](https://github.com/JJWRoeloffs/autobi_py/tree/master/autobi/src/main/java/edu/cuny/qc/speech/AuToBI/featureset) in the original AuToBI, which the adapter gets out with java reflections and runs to get the features they generate out.

#### Extracting a FeatureSet

To actually extract any features from input data, the API gets a little messier. The input expects a `.wav` file and a praat `.TextGrid` file, both _from disk_, meaning the functions take file paths as arguments. AuToBI should also accept different input formats, but I have not tested those.

The necessity of the `.wav` file is probably expected. However, the `.TextGrid` file might be surprising. The reason this is needed is because ToBI is a transcription format that is defined as something to add _on top of_ a normal, textual, transcription, and AuToBI only adds this layer. To get a base transcription in TextGrid format from raw audio, you can, for example, check out another project I wrote for my BA thesis: [transcribe_allign_textgrid](https://github.com/JJWRoeloffs/transcribe_allign_textgrid).

The format AuToBI expects the TextGrids to be in is a grid with a single interval tier, called "words", that contains the force-alligned transcription. It cannot deal with empty intervals, but those can be replaced with dashes instead.

The actual data extraction is done with the `DatasetBuilder`, which takes an argument list from the ArgumentBuilder:

```python
from autobi.core import AutobiJVMHandler
from autobi import ArgumentBuilder, DatasetBuilder

with AutobiJVMHandler() as jvm:
    argument_builder = ArgumentBuilder(jvm)
    argument_builder.with_input_wav(input_wav)
    argument_builder.with_input_TextGrid(input_grid)
    args = argument_builder.to_args_string()

    data = DatasetBuilder(jvm, args)
```

This `DatasetBuilder` should then be told what features to extract. This can, of course, be done by giving it an instance of `FeatureSet`, although it also has the same interface as `FeaturenamesBuilder` to add more to it (The advantage of feature sets being you can pass them around your in code if you want to create multiple data sets)

```python
from autobi.core import AutobiJVMHandler
from autobi import ArgumentBuilder, DatasetBuilder, FeaturenamesBuilder

with AutobiJVMHandler() as jvm:
    builder = FeaturenamesBuilder(jvm)
    builder.with_default_features("PhraseAccentClassificationFeatureSet")
    featureset = builder.build()

    argument_builder = ArgumentBuilder(jvm)
    argument_builder.with_input_wav(input_wav)
    argument_builder.with_input_TextGrid(input_grid)
    args = argument_builder.to_args_string()

    databuilder = DatasetBuilder(jvm, args)
    databuilder.with_feature_set(featureset)
    databuilder.with_feature(r"mean[subregionC[znormC[f0],subregion[200ms]]]")
    databuilder.with_default_features("PitchAccentClassificationFeatureSet")
```

Finally, the data can be extracted. To do this, the output can either be written do csv, arff, or liblinear formats, or exported to a pandas dataframe directly, which simply writes to a csv, and then reads from that csv.

```python
# Please note you can only call one: Calling write invalidates the builder object.
databuilder.write_csv(output_csv)
databuilder.write_arff(output_arff)
databuilder.write_liblinear(output_liblinear)
```

One common pattern you might find yourself using is:

```python
with TemporaryDirectory() as temp_dir:
    tempfile = Path(temp_dir) / "out.csv"
    databuilder.write_csv(tempfile)
    df = pd.read_csv(tempfile, delimiter=",", na_values=["?"]).astype(float)
```

which is added as a buildin function `datasetbuilder.build_pandas()`

## Examples

A file that uses autobi_py to extract features might look a little like this, which is a simplified excerpt from the code I wrote for the actual experiment of my BA thesis (which can be found [here](https://zenodo.org/records/8129129))

```python
import functools
from pathlib import Path
from dataclasses import dataclass

import numpy as np
import pandas as pd

from autobi.core import AutobiJVM, AutobiJVMHandler
from autobi import ArgumentBuilder, DatasetBuilder, FeaturenamesBuilder, FeatureSet


@dataclass
class DataSet:
    accent_detection: pd.DataFrame
    accent_classification: pd.DataFrame


def get_autobi_features(
    grid_file: Path, wav_file: Path, jvm: AutobiJVM, featureset: FeatureSet
) -> pd.DataFrame:
    args = (
        ArgumentBuilder(jvm)
        .with_input_wav(input_wav)
        .with_input_TextGrid(input_grid)
        .to_args_string()
    )
    return DatasetBuilder(jvm, args).with_feature_set(featureset).build_pandas()


def create_features(
    df: DataSet,
    get_accent_detection_features: Callable[[pd.DataFrame], pd.DataFrame],
    get_accent_classification_features: Callable[[pd.DataFrame], pd.DataFrame],
) -> DataSet:
    df.accent_detection = (
        df.accent_detection.groupby("grid_path", group_keys=False)
        .apply(get_accent_detection_features)
        .drop(["wav_path", "grid_path", "start", "end", "word"], inplace=False, axis=1)
        .reset_index(drop=True)
    )

    df.accent_classification = (
        df.accent_classification.groupby("grid_path", group_keys=False)
        .apply(get_accent_classification_features)
        .drop(["wav_path", "grid_path", "start", "end", "word"], inplace=False, axis=1)
        .reset_index(drop=True)
    )
    return df

def feature_creation_autobi(df: DataSet) -> DataSet:
    with AutobiJVMHandler("main") as jvm:
        accent_detection_features = (
            FeaturenamesBuilder(jvm)
            .with_default_features("PitchAccentDetectionFeatureSet")
            .build()
        )
        accent_classification_features = (
            FeaturenamesBuilder(jvm)
            .with_default_features("PitchAccentClassificationFeatureSet")
            .build()
        )

        def get_features(features: FeatureSet, df: pd.DataFrame) -> pd.DataFrame:
            autobi_features = get_autobi_features(
                df["grid_path"].iloc[0],
                df["wav_path"].iloc[0],
                jvm,
                features,
            )
            return pd.concat([df, autobi_features], axis=1, join="inner")

        return create_features(
            df,
            get_accent_detection_features=functools.partial(get_features, accent_detection_features),
            get_accent_classification_features=functools.partial(get_features, accent_classification_features),
        )
```

Code that transforms the output from [transcribe_allign_textgrid](https://github.com/JJWRoeloffs/transcribe_allign_textgrid) to the format that AuToBI expects, making use of the [PraatIO](https://github.com/timmahrt/praatIO) library, might look something like this:

```python
from praatio.data_classes.interval_tier import IntervalTier
from praatio.data_classes.textgrid import TextGrid
from praatio.utilities.constants import Interval


def replace_empty(item: Interval) -> Interval:
    if not item.label:
        return item._replace(label="-")
    return item


def reformat_textgrid(grid: TextGrid) -> TextGrid:
    words = [replace_empty(word) for word in grid.tierDict["words"].entryList]
    new_grid = tg.Textgrid(
        minTimestamp=grid.minTimestamp, maxTimestamp=grid.maxTimestamp
    )
    new_grid.addTier(
        IntervalTier("words", words, minT=grid.minTimestamp, maxT=grid.maxTimestamp)
    )
    return new_grid
```

## Notes on weirdness of style

An attentive reader might have noticed this adapter overuses the Builder pattern and generally has a very weird Python API. This is because of the limitations that come from the Java-Python bridge. The bridge is only sending strings (sometimes serialized as Json) to and from Java. Because of this, the builder pattern is great, as it sends single strings to the JVM at a time, with the `build` method returning only strings to be used for other parts of the API. Moreover, having to call the functions on objects means that those objects can keep a reference to the JVM view themselves.

Similarly, the overuse of the ArgumentBuilder is because AuToBI was originally designed as an application, not a library. Internal Java functions all want an instance of AuToBIArguments, which I construct like this.

A more complete Python project would probably add another layer of abstraction on top of the present library to provide a more Pythonic API.

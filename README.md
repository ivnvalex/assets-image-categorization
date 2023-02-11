# assets-image-categorization
One of the test tasks made during interviews for one of the companies.

Usage:

– Data preprocessing: run parse_json.py, run oversample.py;

– Model training: run train_model.py;

– **Make prediction**: run predict.py. Makes predictions on test_bundle data. Creates lists of Cars and Plants recognized containing dictionaries with 'file', 'probability' keys. Prints class label followed by every element of a corresponding list.

Ex.:

Cars predicted:

{'file': '2873600a-fa17-4625-94c9-0a728b563dab.png', 'probability': 0.9997311}

.
.
.

Plants predicted:

{'file': '7e5ba16b-6223-41f3-8f64-07ea079ece48.png', 'probability': 0.9997192}

![](https://github.com/ivnvalex/image-categorization/blob/main/live-demo.gif)

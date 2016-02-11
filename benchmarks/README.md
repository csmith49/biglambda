#### Signature and Data Specs
This is the directory for storing benchmark details. A benchmark named `bm` has the following folder structure:
```
testdata
+---bm
|   +---sig.py
|   +---data
+---<more benchmarks>
+---<...> 
```
This regularized format allows scripts to perform synthesis tasks with just the name of the benchmark, assuming no other parameters need tweaking.

Type specifications in both data formats must start with a capital letter.

## Signature Specs
The signatures are files of annotated python functions. Introspection allows us to perform type-safe expansion based on the annotations. An example annotation is given below:
```python
def charAt(word : "String", index : "Int") -> "String":
    return word[index]
```
Constants can also be described:
```python
def zero() -> "Int":
    return 0
```
The introspection system looks at everything in the namespace of the signature file, so anything imported will also be inspected. Having un-annotated functions will break the code.

## Data Specs
Data is provided in a semi-structured XML style. Data elements are Python literals, so strings must always be quoted.

The parser is BeautifulSoup4, which can be installed by:
    pip3 install BeautifulSoup4

The parser looks for a few important tags, whose behavior is described below.

**Data**: the data tags wrap the entire file, and have attributes for the input, output, and key synthesis types.
```XML
<data input="INPUT TYPE" output="OUTPUT TYPE" key="OPTIONAL KEY">
    ...
</data>
```
**Example**: the example tags lie inside the data tags, and just wrap individual input/output data pairs.
```XML
<example>
    ...
</example>
```
**Weight**: the weight tag lies inside the data tags. It provides a mechanism for preferring one item in your signature over another. Just specify the name of the component and give it a floating-point value greater than zero (and not too small, or underflow might be an issue). Larger numbers mean the component is more likely to be seen.
```XML
<weight name="COMPONENT NAME" val=FLOAT>
```
**Input**: the input tag lies inside the example tags. Any _input_ tag outside a pair of _example_ tags will be ignored. An optional attribute is _delim_, which allows you to choose how you want the data split.
```XML
<input>
    1
    2
    3
</input>
...
<input delim=","> 1, 2, 3 </input>
```
**Output**: the output tag can be used identically to the _input_ tag if your synthesis task is generating a list of values (like for keyed synthesis). Otherwise, you can specify the _val_ attribute to provide just a single value. Just like _input_, any tags outside _example_ tags will be ignored.
```XML
<output>
    ("ID10001", "Bob", 12)
    ("ID10002", "Alice", 73)
    ("ID10003", "Charlie", 2)
</output>
...
<output val=6>
```

A sample data file is presented below (for a sum task):
```XML
<data input="Int" output="Int">
    <weight name="add" val=10>
    <example>
        <input delim=","> 1, 2, 3 </input>
        <output val=6>
    </example>
    <example>
        <input delim=","> 10, 57, 23 </input>
        <output val=90>
    </example>
</data>
```

## Benchmarks
Simple Numerical Operators (11):
* *Sum*: sum of all inputs
* *Min/Max*: min/max of all inputs
* *Round->Sum*: round all inputs, then add
* *Sum->Round*: add, then round the result
* *Square->Sum*: computes sum of squares
* *Sum->Square*: computes square of sums
* *Histogram*: binning based on some rounding operator
* *Statistics*: computation of standard deviation
* *Factor-Counting*: counts the number of a given prime factor
* *Sum-of-Factors*: factors all inputs, then adds the results
* *Unique*: pulls out all unique items (turns to a set)

Text Manipulations (11):
* *Word-Count*
* *PoS-Tag-Counting*: given a component that does PoS tagging, count occurence of tags
* *Anagrams*: finds anagrams in input lists
* *GREP*
* *Date-Extraction*
* *Word-Length-Stats*
* *Letter-Frequency-Analysis*: histogram and/or other stats on letter frequencies
* *Hashtag-Stats*: cooccurrences of hashtags in tweets
* *Cooccur*: word-based cooccurrence analysis
* *Inverted-Index*
* *Bigrams/Trigrams*

Relational Database (4):
* *Selection*
* *Union*
* *Intersection*
* *Difference*

Hard Stuff (6):
* *Average*: computes average of all numbers (surprisingly hard)
* *MSS*: maximum-segment-sum, and other marking list homomorphisms
* *Bracket-Matching*
* *Page-Rank*: a single iteration of the Page-Rank algorithm
* *Clustering*: single iteration of a k-means clustering algorithm
* *Classification*: given clusters, classify all data points


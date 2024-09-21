# ustache (deprecated)

Mustache for Python, backwards-compatible wrapper of [mstache](https://gitlab.com/ergoithz/mstache).

- Current documentation (mustache): [mstache.readthedocs.io](https://mstache.readthedocs.io)
- Old documentation: [ustache.readthedocs.io](https://ustache.readthedocs.io)

> :warning: Development moved over to [mstache](https://gitlab.com/ergoithz/mstache),

## Installation

```sh
$ pip install ustache
```

## Usage

Python:

```python
import ustache

print(ustache.render('Hello {{v}}', {'v': 'World!'}))
# Hello World!
```

Command line:

```sh
$ ustache -j data.json -o output.html template.mustache
```

## Highlights

- The fastest pure-python Mustache implementation to this date.
- Command line interface.
- Spec compliant, but also highly compatible with `Mustache.js`.
- Small codebase, efficiently rendering to `str` or `bytes`,
  supporting streaming.
- Customizable (property getter, partial resolver, and stringify, escape
  and lambda render functions).
- Customizable template caching, with an optional memory-efficient mode
  (see [xxhash optional dependency below](#xxhash)).
- No dynamic code generation, jit and transpiler friendly.

## Considerations

For inter-compatibility with JavaScript (especially `Mustache.js`, enabling
client-side rendering with the same templates), **ustache** exposes some
atypical behavior:

- Mustache blocks stick to JavaScript falseness (`__bool__` is not honored):
  `None`, `False`, `0`, `nan`, and empty sequences (including strings)
  are taken as falsy, while everything else (including empty mappings) will
  be considered truthy (`Mustache.js` `Boolean` and empty `Array` handling).
- Mustache blocks receiving any iterable other than mappings and strings
  will result on a loop (`Mustache.js` `Array` handling).
- Non-mapping sized objects will expose a virtual `length` property
  (JavaScript `Array.length` emulation).
  Customizable via `getter` parameter.
- Mapping keys containing dot (`.`) or whitespace (` `) are unreachable,
  (`Mustache.js` property name limitation).
  Customizable via `getter` parameter.
- Sequence elements are accessible by positive index in the same way mapping
  integer-keyed items are also accessible when no string key conflicts, as
  properties (JavaScript `Object` emulation).
  Customizable via `getter` parameter.

## Optional dependencies

For minimalism and portability, **ustache** has no hard dependencies, while
still supporting some libraries for added functionality:

- <a id="xxhash"></a>[xxhash](https://pypi.org/project/xxhash)
  will be used, if available, to avoid storing the whole template data as
  part of the template cache, dramatically reducing its memory footprint in
  many situations.

Optional but generally recommended dependencies can be easily installed
all at once using **ustache** `optional` extra target:

```sh
$ pip install ustache[optional]
```

## Syntax

Check out the [mustache(5) manual](https://mustache.github.io/mustache.5.html).

For quick reference, here is a quick overview of the Mustache syntax.

Template (`template.mustache`):
```handlebars
{{!comment}}
<ul>
{{#object}}<li>{{property}}</li>{{/object}}
{{^object}}<li>As <b>object</b> is truthy, this won't be shown</li>{{/object}}
{{^null}}<li><b>null</b> is falsy</li>{{/null}}
{{#array}}<li>{{property}}</li>
{{/array}}
{{^array}}<li>Array isn't empty, this won't be shown.</li>{{/array}}
{{#empty_array}}<li>Empty Array, this won't be shown</li>{{/empty_array}}
{{^empty_array}}<li>empty_array is empty</li>{{/empty_array}}
{{&unescaped_html}}
</ul>
```

Data (`data.json`):
```json
{
  "object": {
    "property": "Object property value"
  },
  "null": null,
  "array": [
    {"property": "Array item1 property"},
    {"property": "Array item2 property"},
    {"property": "Array item3 property"}
  ],
  "empty_array": [],
  "unescaped_html": "<li>this is unescaped html</li>"
}
```

Command:
```sh
$ ustache -j data.json -o output.html template.mustache
```

Output:
```html
<ul>
<li>Object property value</li>
<li><b>null</b> is falsy</li>
<li>Array item1 property</li>
<li>Array item2 property</li>
<li>Array item3 property</li>
<li>empty_array is empty</li>
<li>this is unescaped html</li>
</ul>
```

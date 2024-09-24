# esdateutil

Provides utilities for handling dates like how Elasticsearch does.

In particular:
 - Datemath parsing and evaluation ([ES Datemath Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math))
 - Datetime string format parsing ([ES Dateformat Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html))
 - (SoonTM) Watcher trigger schedule duration evaluation

The goals of this project are:
 - Be as close to Elasticsearch behaviour as Python makes sensible.
 - No mandatory runtime dependencies.
 - Customizability; most functionality should be parameterizable.

## Examples

### Basic Usage
```py
>>> from datetime import datetime
>>> datetime.now() # now is as below for all examples
datetime.datetime(2024, 9, 24, 8, 36, 17, 503027)

>>> from esdateutil import datemath, dateformat

>>> df = dateformat.DateFormat() # defaults to strict_date_optional_time||epoch_millis
>>> df.parse("2024-09-24T08:36Z") # strict_date_optional_time
datetime.datetime(2024, 9, 24, 08, 36, tzinfo=datetime.timezone.utc)
>>> df.parse("1727163377503") # epoch_millis
datetime.datetime(2024, 9, 24, 8, 36, 17, 503000)

>>> dm = DateMath()
>>> dm.eval("now-5m/h") # now minus 5 minutes rounded to the hour
datetime.datetime(2024, 9, 24, 8, 0)
>>> dm.eval("2024-09-24||-5m/h") # absolute time minus 5 minutes rounded to the hour
datetime.datetime(2024, 9, 23, 23, 0)
```

## Roadmap

This project will be version 1.0 when it provides:
 - Parsing for watcher schedule definitions, excluding cron expressions
 - A parse_math and eval_math function in datemath to handle math expressions that don't include a date anchor
 - Robust tests for weird stuff like datemath rounding on DST boundaries in 3.3, 3.5, 3.8+
 - Thread safety and tests thereof

See also the [TODO file](./TODO).

## Links

https://pypi.org/project/esdateutil/

## Building

Requires pyenv and pyenv-virtualenv to be installed on your machine.
Requires pyenv-init (pyenv and pyenv-virtualenv) to be run for pyenv local to work w/ virtualenv

## Differences from Elasticsearch

One of the consequences of using Python's built-in datetime objects and
functions by default is that they can behave very differently from version to
version and from Elasticsearch defaults. Below are some of the most important
differences in functionality to be aware of.

 - The default time resolution in Elasticsearch is milliseconds, whereas in
   Python datetime it is microseconds. This shouldn't be important unless you
   are using datemath.UNITS_ROUND_UP_MICROS or another custom round
   implementation. UNITS_ROUND_UP_MILLIS is provided as an alternative.
 - Elasticsearch has optional support for nanosecond precision - because Python
   datetimes use microsecond precision, we cannot support this completely. This
   impacts dateformat strict_date_option_time_nanos, which can still be used
   for microsecond precision instead of millis precision.
 - For custom dateformat strings we use strptime as a backup instead of [Java's time format strings](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html).

## Alternatives

### python-datemath

There is another Python project
[python-datemath](https://pypi.org/project/python-datemath/) for parsing
datemath expressions. This projects has different goals to esdateutil, the main
difference between them is that python-datemath parses a custom datemath
variant, whereas esdateutil.datemath adheres strictly to the Elasticsearch
datemath syntax. This means that although the syntax overlaps they will accept
and reject different strings.

In most cases, this probably doesn't matter. See the table below for a specific
feature difference breakdown.

| Difference          | esdateutil.datemath                              | python-datemath                                                                                                                                                                                                                                                                                          |
| -----------         | ----------                                       | ---------------                                                                                                                                                                                                                                                                                          |
| Syntax              | Accepts and rejects same syntax as Elasticsearch | Allows additional unit chars (Y for year, D for day, S for second), allows long-form units (e.g. `seconds`, `days`), allows fractional durations (e.g. +1.2d), does not allow missing number (e.g. +y vs +1y), treats expressions without anchors as having `now` (e.g. `+2d` is equivalent to `now+2d`) |
| Date String Support |                                                  | Accepts second epochs by default.                                                                                                                                                                                                                                                                        |
| Types               |                                                  |                                                                                                                                                                                                                                                                                                          |
| Dependencies        | None.                                            | 4, including transitive dependencies: arrow --> python-dateutil --> six + types-python-dateutil                                                                                                                                                                                                          |
| Version Support     |                                                  |                                                                                                                                                                                                                                                                                                          |
| Type Hints          |                                                  |                                                                                                                                                                                                                                                                                                          |
| Thread Safety       |                                                  |                                                                                                                                                                                                                                                                                                          |
| Timezones           |                                                  |                                                                                                                                                                                                                                                                                                          |
| Options             |                                                  | https://github.com/nickmaccarthy/python-datemath/blob/master/datemath/helpers.py#L85                                                                                                                                                                                                                     |
| Logging             |                                                  |                                                                                                                                                                                                                                                                                                          |

For those that care, based on some not very rigorous profiling, as of writing
esdateutil's `DateMath.eval` is between 9-10x faster than python-datemath's
equivalent `dm` for an arbritrary set of strings, mostly due to overhead from
the arrow library.

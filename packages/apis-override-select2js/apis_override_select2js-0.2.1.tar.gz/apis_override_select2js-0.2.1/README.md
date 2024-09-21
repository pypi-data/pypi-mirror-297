Override select2js files in APIS Django projects
================================================

This is a minimal Django project that ships 2 files that are originally part of
[Django Autocomplete
Light](https://github.com/yourlabs/django-autocomplete-light).
The two files are patched, so that they fix a behaviour with the `tags` option
of the select implementation in Django Autocomplete Light. See also [this bug
report
upstream](https://github.com/yourlabs/django-autocomplete-light/issues/902).
The exact changes are documented in [contrib/patches](contrib/patches).

If you want to override the upstream shipped javascript files, you will have
install this Django project and add `apis_override_select2js` to the beginning
of your Django settings `INSTALLED_APPS`.

You will get a warning from Django when doing the `collectstatic` step:
```
Found another file with the destination path
'autocomplete_light/select2.min.js'. It will be ignored since only the first
encountered file is collected. If this is not what you want, make sure every
static file has a unique path.
Found another file with the destination path 'autocomplete_light/select2.js'.
It will be ignored since only the first encountered file is collected. If this
is not what you want, make sure every static file has a unique path.
 ```

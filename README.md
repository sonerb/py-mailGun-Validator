# py-mailGun-Validator

This is [mailGun][1] Mail List Validator

### Usage
```sh
validate_email.py -i input_list.txt -o output_list.txt -f (force start) -t (thread Count) 
```

### Config
* [Sign Up][2] free.
* Get your public api key in [control panel][3]
* Change your `public api key` line 17.

```python
self.api_key             = 'pubkey-5ogiflzbnjrljiky49qxsiozqef5jxp7'
```

[1]: https://documentation.mailgun.com/api-email-validation.html#example
[2]: https://mailgun.com/signup
[3]: https://mailgun.com/app/dashboard

# Alfred Pastebin
<p>
<img src="https://img.shields.io/github/v/release/earthpyy/alfred-pastebin">
<img src="https://img.shields.io/github/workflow/status/earthpyy/alfred-pastebin/Python%20application">
</p>

</p>
Automatically create a new paste in Pastebin.com from your clipboard
</p>


## Requirements
- Alfred 4
- Powerpack
- Python 3+


## Installation
1. Download latest release [here](https://github.com/earthpyy/alfred-pastebin/releases/latest)
2. Double-click to add to **Alfred**
3. Go to [Pastebin API page](https://pastebin.com/doc_api#1) and copy the key in the section named _Your Unique Developer API Key_
4. Open _Alfred_, go to _workflow environment variables_ and put the copied key into variable `API_DEV_KEY`

### Guest Mode
By default, this workflow will paste your content as a guest.

If you want to paste on your account you need to enter your Pastebin username and password in variable `API_USER_NAME` and `API_USER_PASSWORD`, respectively.


## Usage
```
pb [name] [language]
```

### Note
- `name` and `language` are optional
- `(CMD + Enter)` to create as unlisted paste (by default)
- Please be careful on unlisted or private paste since a free Pastebin account has a paste limit on those two types of permission


### Workflow Environment Variables
- USER_KEY : 'api_user_key' of Pastebin account
- EXPIRE_DATE : default expire date of a paste (default: 1 week)

| Name | Default | Required | Description |
| ---- | ------- | -------- | ----------- |
| `API_DEV_KEY` | - | Yes | [Your Unique Developer API Key](https://pastebin.com/doc_api#1) |
| `API_USER_NAME` | - | No | Your Pastebin username (see: [Guest Mode](#guest-mode)) |
| `API_USER_PASSWORD` | - | No | Your Pastebin password (see: [Guest Mode](#guest-mode)) |
| `DEFAULT_NAME` | `Untitled` | Yes | Default paste name if not defined |
| `DEFAULT_PERMISSION` | `public` | Yes | Paste permission (available value: `public`, `unlisted`, `private`) |
| `CMD_PERMISSION` | `unlisted` | Yes | Paste permission if you hold `CMD` |
| `EXPIRE_DATE` | `1W` | Yes | Paste expiration date ([available value](https://pastebin.com/doc_api#6)) |


## Like it?
<a href="https://paypal.me/earthpyy" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

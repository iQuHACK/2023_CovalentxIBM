from julian_code import is_pokemon_legendary
from fastapi.responses import HTMLResponse
import uvicorn

from typing import List
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get():
    return HTMLResponse('''
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="UTF-8" />
    <title>Quantum Pokemon</title>
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"
    />
    <meta name="format-detection" content="telephone=no" />
    <meta name="msapplication-tap-highlight" content="no" />
  </head>
  <body>
    <ion-app>
      <ion-header>
        <ion-navbar>
          <ion-title style="padding: 10px">Quantum AI Blockchain Nuclear Fusion Pokemon</ion-title>
        </ion-navbar>
      </ion-header>

      <ion-content padding>
      	<div style="margin: 10px">Enter your Pokemon's stats</div>
        <div id="user_input" style="margin: 10px; border: 1px solid rgb(204, 204, 204) !important; border-radius: 5px; padding: 2px">
		<ion-item>
		  <ion-label>HP: </ion-label>
		  <ion-input id="hp"></ion-input>
		</ion-item>
		<ion-item>
		  <ion-label>Attack: </ion-label>
		  <ion-input id="att"></ion-input>
		</ion-item>
		<ion-item>
		  <ion-label>Defense: </ion-label>
		  <ion-input id="def"></ion-input>
		</ion-item>
		<ion-item>
		  <ion-label>Sp Attack: </ion-label>
		  <ion-input id="spatt"></ion-input>
		</ion-item>
		<ion-item>
		  <ion-label>Sp Defense: </ion-label>
		  <ion-input id="spdef"></ion-input>
		</ion-item>
		<ion-item>
		  <ion-label>Speed: </ion-label>
		  <ion-input id="speed"></ion-input>
		</ion-item>
		<ion-button onClick="send_data()">Check Pokemon</ion-button>
        </div>
        <div id="result" style="margin: 10px; border: 1px solid rgb(204, 204, 204) !important; border-radius: 5px; padding: 2px"></div>
      </ion-content>
    </ion-app>


    <!-- Import the Ionic CSS -->
<link href="https://unpkg.com/@ionic/core@latest/css/ionic.bundle.css" rel="stylesheet"><!-- Import Ionic -->
<script src="https://unpkg.com/@ionic/core@latest/dist/ionic/ionic.js"></script><!-- Optional, import the Ionic icons -->

<script type="module" src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.esm.js"></script>
<script nomodule="" src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.js"></script>


<script>
function send_data(){
// post body data
const user = {
  hp: document.getElementById('hp').value,
  att: document.getElementById('att').value,
  def: document.getElementById('def').value,
  spatt: document.getElementById('spatt').value,
  spdef: document.getElementById('spdef').value,
  speed: document.getElementById('speed').value,
}

// request options
const options = {
  method: 'POST',
  body: JSON.stringify(user),
  headers: {
    'Content-Type': 'application/json'
  }
}

// send POST request
fetch('get_result', options)
  .then(res => res.json())
  .then(res => document.getElementById('result').innerHTML = "Your Pokemon is: "+res.result)
}
</script>

  </body>
</html>''')
'''
<script type="module" src="node_modules/@ionic/core/dist/ionic/ionic.esm.js"></script>
<script nomodule src="node_modules/@ionic/core/dist/ionic/ionic.js"></script>
<link rel="stylesheet" href="node_modules/@ionic/core/css/ionic.bundle.css"/>
'''

@app.post("/get_result")
def root(stats: dict[str,str]):
	return {'status':'success',
		'result':is_pokemon_legendary(stats)}


if __name__ == "__main__":
	uvicorn.run("server:app", host="localhost", port=8000, reload=True)

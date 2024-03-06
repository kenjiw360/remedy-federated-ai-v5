const express = require("express");
const busboy = require("connect-busboy");
const path = require('path');
const fs = require("fs");

const app = express();

app.use(express.static("./"));
app.use(busboy())

app.post('/upload', function (req, res){
	console.log('should start uploading');
	if(req.busboy){
		console.log("we have busboy")
		req.busboy.on('file', (name, file, info) => (console.log('received file from request'), file.on('data', data => (console.log('received data from file', data)))));
	
		req.busboy.on('close', () => {
			console.log(fileData);
			res.send('finished uploading!');
		});
	}
});


app.listen(3000);

let loadedHikesStrData = "";
let hikesTableData = {};
let hikesSheetData = {};

function hasOwnProperty(obj, prop) {
	var proto = obj.__proto__ || obj.constructor.prototype;
	return (prop in obj) &&
		(!(prop in proto) || proto[prop] !== obj[prop]);
}


function loadClient() {
	gapi.client.setApiKey("AIzaSyBwRky_pwhrRnkmBKWt17Jz8XItbOijMOI");
	return gapi.client.load("https://sheets.googleapis.com/$discovery/rest?version=v4")
		.then(function () {

			console.log("GAPI client loaded for API");
			execute();


		},
			function (err) { console.error("Error loading GAPI client for API", err); });
}


function execute() {
	return gapi.client.sheets.spreadsheets.get({
		"spreadsheetId": "1IG3-IDP8UX5C_vFEPasYYIe9kUuFY-HpmwhRT4welTM",
		"includeGridData": true,
		"ranges": [
			"A1:J40"
		]
	})
		.then(function (response) {
			// Handle the results here (response.result has the parsed body).
			// console.log("Response", response);
			loadedHikesStrData = response;
			// console.log("DATA ::: ", loadedHikesStrData);
			hikesTableData = JSON.parse(loadedHikesStrData.body);
			// console.log(hikesTableData);

			hikesSheetData = hikesTableData.sheets[0].data[0].rowData;
			// console.log(hikesSheetData);
			draw(hikesSheetData);

		},
			function (err) { console.error("Execute error", err); });

}

function draw(hikesSheetData) {
	let tb = hikesSheetData;

	tb[0].values.forEach((element) => {
		var $div = $("<th>", { "class": "hk_heading" });
		$div.text(element.formattedValue);
		$("#hk_properties").append($div);
	});

	let startSeasonRow = 1;
	let currentRow = 1;

	while (currentRow < tb.length && hasOwnProperty(hikesSheetData[currentRow].values[1], "formattedValue")) {

		let row_height_counter = 0;
		let $row = $("<tr>", { "class": "hk_line", "scope":"row", id: "hk_line_" + currentRow });

		if (hasOwnProperty(hikesSheetData[currentRow].values[0], "formattedValue")) {
			let rowspanCounter = 1;
			if (currentRow + rowspanCounter < tb.length) {
				while (!hasOwnProperty(hikesSheetData[currentRow + rowspanCounter].values[0], "formattedValue")) {

					rowspanCounter++;

					if (currentRow + rowspanCounter >= tb.length) {
						break;
					}
				}
			}

		var $div = $("<th>", { "class": "hk_heading vertical-text", "scope":"row", "rowspan": rowspanCounter });
		$div.text(tb[currentRow].values[0].formattedValue);
		$($row).append($div);


		}

		for (let i = 1; i < tb[currentRow].values.length; i++) {
			var $prop = $("<td>", { "class": "hk_value",  "scope":"col" });
			$prop.text(tb[currentRow].values[i].formattedValue);
			$($row).append($prop);			
		}


		$("#hk_body").append($row);
		currentRow++;
	}

}


$(window).on('load', function () {

	gapi.load("client");
	loadClient();

})




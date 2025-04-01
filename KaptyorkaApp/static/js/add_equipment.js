let trees = $("select#demo2").treeMultiselect({
	searchable: true,
	searchParams: ["section", "text"],
	onChange: treeOnChange,
	freeze: true,
	startCollapsed: true,
})

let tree = trees[0]
var totalPrice = 0
var newItemsNumber = 0
var newFoldersNumber = 0

class Equipment {
	constructor(name = "", path = "") {
		this.id = 0
		this.name = name
		this.path = path
		this.desc = ""
		this.price = 0.0
		this.amount = 1
	}
}

$(function () {
	reloadTree();
	$("[data-description='Folder']").hide()
})

function getPath(element) {
	obj_path = ""
	el_parent = element
	while (el_parent.nodeName != "BODY") {
		if (el_parent.className.search("section") != -1) {
			if ($(el_parent).children(".title").length > 0) {
				elParentCat = $(el_parent).children(".title")[0].innerText
			} else {
				elParentCat = $(el_parent).children("div.flex-title").children(".title")[0].innerText
			}

			if (obj_path == "") {
				obj_path = elParentCat
			} else {
				obj_path = elParentCat + "/" + obj_path
			}
		}
		el_parent = el_parent.parentElement
	}
	return obj_path
}

function reloadTree() {
	tree.reload();
	addCatButton();

	updateAllItemsInCartWithControls();
	updateAllItemsInCatalogWithControls();

	if (exists("#selectedEquipmentBlock")) byId('selectedEquipmentBlock').remove();
	$(".tree-multiselect .selected").append("<div id='selectedEquipmentBlock'></div>");

	if (exists("#controlBlock")) byId('controlBlock').remove();
	$(".tree-multiselect .selected").append("<div id='controlBlock'></div>");


	if (exists("#controlBlockSeparator")) byId('controlBlock').remove();
	$(".tree-multiselect .selected").append("<div id='controlBlockSeparator'></div>");

	if (!exists("#controlBlockHr")) $("#controlBlockSeparator").append("<hr id='controlBlockHr'>");

	$("div").find(`[data-description='Folder']`).hide();
}

function treeOnChange(allSelectedItems, addedItems, removedItems) {
	updateAllItemsInCartWithControls();
	countTotalPrice();
}


function updateAllItemsInCartWithControls() {
	$(".tree-multiselect .selected .item").toArray().forEach(updateItemInCartWithControls);
}	

function updateItemInCartWithControls(line) {
	eqId = line.getAttribute("data-value");
	
	// check if this item is it the cart
	if (line.childElementCount < 3) {
		var price = prices[eqId][0];
		totalPrice += Number(price);	
	
		line.id = eqId + "selectedLine";

		$("#" + line.id).prepend("<label>" + line.childNodes[0].textContent + "</label>");
		line.childNodes[1].textContent = "";

		sName = line.querySelector(".section-name");
		line.lastChild.remove();
		$("#" + line.id).append("<span class='price-col'>" + price + "₴</span>");
		$("#" + line.id).append(`<p class="amount-limit">/` + prices[eqId][1] + `шт.</p>`);
		$("#" + line.id).append(`<input id="amount_` + eqId + `" class="amount-selector dark" type="number" min="1" max="` + prices[eqId][1] + `" step="1" value="1" onchange="countTotalPrice()">`);
	}
}

function countTotalPrice() {
	totalPrice = 0;
	$(".tree-multiselect .selected .item").toArray().forEach(countTotalPrice);
	// selectedEquipmentToJSON();
	$("#priceField")[0].innerText = "Итоговая цена: " + totalPrice + "₴";
	$("#priceCDataField")[0].innerText = "Итоговая амортизация: " + totalPrice + "₴";

	$("#priceHiddenField")[0].value = totalPrice;
	function countTotalPrice(line) {
		eqId = line.getAttribute("data-value");
		var price = prices[eqId][0];

		totalPrice += Number(price) * Number($("#amount_" + eqId)[0].value);
	}
}

function scrollToProps() {
	const mediaQuery = window.matchMedia("(max-width: 481px)")

	if (mediaQuery.matches) {
		const element = document.querySelector("div.tree-multiselect div.selected")
		element.scrollIntoView({
			behavior: "smooth", // Smooth scroll
			block: "start", // Scroll to the top of the element
		})
	}
}

function createNewItemMenu(path) {

	let selectedOpt = $("#controlBlock");

	$(selectedOpt).empty()
	$(selectedOpt).append(`<input type="hidden" id="newItemPath" value=` + path + `></input>`)
	$(selectedOpt).append("<h4 id='addEquipmentHeader'>Додати снар в " + path + "</h4>")
	$(selectedOpt).append(`<label for="leadLabel">Назва</label>`)
	$(selectedOpt).append(`<input type="text" class="form-control dark" id="newItemName" placeholder="Terra Incognita Canyon 3 Alu">`)
	$(selectedOpt).append(`<small id="leadInputHelp" class="form-text text-muted">Назва, виробник і модель.</small><br>`)

	$(selectedOpt).append(`<label for="leadLabel">Опис</label>`)
	$(selectedOpt).append(`<textarea class="form-control dark" id="newItemDesc" rows="4" placeholder="Надміцні сталеві дуги, три з них зламані"></textarea>`)
	$(selectedOpt).append(`<small id="leadInputHelp" class="form-text text-muted">Виключні властивості цього(-их) объекта(-ів).</small><br>`)

	$(selectedOpt).append(`<label for="leadLabel">Кількість</label>`)
	$(selectedOpt).append(`      
	<div class="input-number">
		<input id="newItemNumber" type="number" min="1" max="100" step="1" value="1">
  	</div>`)
	$(".input-number input[type='number']").inputSpinner()
	$(selectedOpt).append(`<small id="leadInputHelp" class="form-text text-muted">1, якщо цей снар унікален у своїй суті.</small><br>`)

	$(selectedOpt).append(`<label for="leadLabel">Плата</label>`)
	$(selectedOpt).append(`      
	  <div class="input-number">
		  <input class="form-control dark" id="newItemPrice" type="number" min="0" max="31415" step="1" value="1"> ₴
		</div>`)
	$(selectedOpt).append(`<small id="leadInputHelp" class="form-text text-muted">Нинада</small><br>`)
	$(selectedOpt).append(`<button class="btn btn-outline-warning" onclick="reloadTree()">Ннє</button>`)
	$(selectedOpt).append(`<button id="sendRequestBtn" class="btn btn-outline-primary" onclick="addNewEquipment()">Нде</button>`)

	scrollToProps();
}

function createNewFolderMenu(path) {
	let selectedOpt = $("#controlBlock");
	$(selectedOpt).empty();
	$(selectedOpt).append(`<input type="hidden" id="newFolderPath" value=` + path + `></input>`);
	$(selectedOpt).append("<h4>Додати нову папку в " + path + "</h4>");
	$(selectedOpt).append(`<label for="leadLabel">Назва</label>`);
	$(selectedOpt).append(`<input type="text" class="form-control dark" id="newFolderName" placeholder="напр., Карємати">`);
	$(selectedOpt).append(`<button class="btn btn-outline-warning" onclick="reloadTree()">Відхилити</button>`);
	$(selectedOpt).append(`<button class="btn btn-outline-primary" onclick="addNewFolder()">Додати</button>`);
}

function addNewEquipment() {
	id = "new_eq_" + newItemsNumber;

	eq_name = document.getElementById("newItemName").value;
	eq_path = document.getElementById("newItemPath").value;

	let newEquipment = new Equipment(eq_name, eq_path);
	newEquipment.id = newItemsNumber;
	newEquipment.desc = document.getElementById("newItemDesc").value;
	if (newEquipment.desc == "") {
		newEquipment.desc = "---";
	}
	newEquipment.amount = document.getElementById("newItemNumber").value;
	newEquipment.price = document.getElementById("newItemPrice").value;

	send_new_equipment("add", "equipment", newEquipment);
	newItemsNumber++;
	reloadTree();
}

function editEquipment(itemId, itemPath) {
	eq_name = document.getElementById("newItemName").value;
	eq_path = document.getElementById("newItemPath").value;

	let updatedEquipment = new Equipment(eq_name, eq_path);

	updatedEquipment.id = itemId.replace("eq_", "");
	updatedEquipment.desc = document.getElementById("newItemDesc").value;
	if (updatedEquipment.desc == "") {
		updatedEquipment.desc = "---";
	}
	updatedEquipment.path = itemPath
	updatedEquipment.amount = document.getElementById("newItemNumber").value;
	updatedEquipment.price = document.getElementById("newItemPrice").value;

	send_new_equipment("update", "equipment", updatedEquipment);
	reloadTree();
}

function addNewFolder() {
	id = "new_fd_" + newFoldersNumber;
	newFoldersNumber++;

	eq_name = document.getElementById("newFolderName").value.replaceAll(" ", " ­");
	eq_path = document.getElementById("newFolderPath").value;

	let newFolder = new Equipment(eq_name, eq_path);
	newFolder.desc = "Folder";
	newFolder.amount = 0;
	newFolder.price = 0;

	$("select#demo2").append("<option readonly style='display:none' value='" + id + "' data-section='" + newFolder.path + "/" + newFolder.name + "' selected='selected' data-description='" + newFolder.desc + "'>" + newFolder.name + "</option>");

	prices[id] = [0, 0];
	reloadTree();
}

function deleteEquipment(id) {
	$("select#demo2 option[value='" + id + "']")[0].remove();
	let newEquipment = new Equipment("", "");
	newEquipment.id = id.replaceAll("eq_", "");
	send_new_equipment("remove", "equipment", newEquipment);
	reloadTree();
}

function send_new_equipment(requestType, objType, obj = "") {
	$.ajax({
		url: "/equipment/add_equipment/",
		type: "POST",
		data: {
			requestType: requestType,
			objType: objType,
			obj: obj,
		},
		//DO NOT EDIT!
		beforeSend: function (xhr, settings) {
			function getCookie(name) {
				var cookieValue = null
				if (document.cookie && document.cookie != "") {
					var cookies = document.cookie.split(";")
					for (var i = 0; i < cookies.length; i++) {
						var cookie = jQuery.trim(cookies[i])
						// Does this cookie string begin with the name we want?
						if (cookie.substring(0, name.length + 1) == name + "=") {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
							break
						}
					}
				}
				return cookieValue
			}
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
			}
		},
		//EDITABLE CODE
		success: function a(json) {
			// alert(json);
			// alert(json.exist);
			if (json.result === "success") {
				if (requestType == "add") {
					new_id = "eq_" + json.new_id
					$("select#demo2").append("<option readonly value='" + new_id + "' data-section='" + obj.path + "' selected='selected' data-description='" + obj.desc + "'>" + obj.name + "</option>")
					prices[new_id] = [obj.price, obj.amount]
				} else if (requestType == "update") {
					itemOption = $("select#demo2")[0].querySelector("option[value='eq_" + obj.id + "']")
					itemOption.setAttribute("data-description", obj.desc)
					itemOption.setAttribute("data-section", obj.path)
					itemOption.innerText = obj.name
					prices["eq_" + obj.id] = [obj.price, obj.amount]
				}
				// alert("Ну, чё. Намана");
				reloadTree()
			} else {
				alert("Изменения не сохранены")
				alert("Ошибка сегментации диска. Компьютер будет перезагружен.")
			}
		},
	})
}

$(function () {
    $('.btn-scrollable').on('click', function () {
        btnId = $(this).attr('id');
        $('.btn-scrollable.active-tab-label').removeClass('active-tab-label').addClass('hidden-tab-label');
        $(this).addClass('active-tab-label').removeClass('hidden-tab-label').blur();
        var menuId = btnId.substring(4, btnId.length);
        $('[href="#' + menuId + '"]').tab('show');
        $('.tab-pane').removeClass('in').removeClass('active').removeClass('show');
        $('#' + menuId).addClass('in').addClass('active').addClass('show');
        $.fn.switchControlTabsButtons();
        updateData();
    });

    $('.next-step, .prev-step').on('click', function (e) {
        var $activeTab = $('.tab-pane.active');
        if ($(e.target).hasClass('next-step')) {
            var nextTabId = $activeTab.next('.tab-pane').attr('id');
            if (nextTabId != undefined) {
                var activeTabId = $activeTab.attr('id');

                var btn = $('#btn-' + activeTabId);
                $('#btn-' + activeTabId).removeClass('active-tab-label').addClass('hidden-tab-label');
                var btn2 = $('#btn-' + nextTabId);
                $('#btn-' + nextTabId).removeClass('hidden-tab-label').addClass('active-tab-label');
                $('#' + activeTabId).removeClass('in').removeClass('active').removeClass('show');
                $('#' + nextTabId).addClass('in').addClass('active').addClass('show');
            }
        }
        else {
            var prevTabId = $activeTab.prev('.tab-pane').attr('id');
            if (prevTabId != undefined) {
                var activeTabId = $activeTab.attr('id');
                var btn = $('#btn-' + activeTabId);
                $('#btn-' + activeTabId).removeClass('active-tab-label').addClass('hidden-tab-label');
                var btn2 = $('#btn-' + prevTabId);
                $('#btn-' + prevTabId).removeClass('hidden-tab-label').addClass('active-tab-label');
                // $('[href="#' + prevTabId + '"]').tab('show');
                $('#' + activeTabId).removeClass('in').removeClass('active').removeClass('show');
                $('#' + prevTabId).addClass('in').addClass('active').addClass('show');
            }

        }
        $.fn.switchControlTabsButtons();
        updateData();
    });

    $.fn.switchControlTabsButtons = function () {
        var $activeTab = $('.tab-pane.active');
        var nextTabId = $activeTab.next('.tab-pane').attr('id');
        if (nextTabId == undefined) {
            $('.next-step').hide();
            $('.last-step').show();
        }
        else {
            $('.next-step').show();
            $('.last-step').hide();
        }
        var prevTabId = $activeTab.prev('.tab-pane').attr('id');
        if (prevTabId == undefined) {
            $('.prev-step').prop('disabled', true);
        }
        else {
            $('.prev-step').prop('disabled', false);
        }
    }

});

function updateData() {

    

    if (true == false) {
        // TIME 
        $("#datesOfRentCDataField")[0].innerText = beauty_date_interval(byId("start_day").value, byId("end_day").value);
        console.log(3);
        // MEMBERS
        var newOnes = byId("newOnes").value;
        var students = byId("students").value;
        var realMembers = byId("realMembers").value;
        var others = byId("others").value;
        var total = parseInt(newOnes) + parseInt(students) + parseInt(realMembers) + parseInt(others);
        $("#selectedEquipmentCDataField .row").remove();
        Array.from($(".tree-multiselect .selected")[0].childNodes).forEach(function (equipment) {
            var dataCDataItem = $(equipment).clone();
            var id = dataCDataItem[0].getAttribute("data-value");
            // dataCDataItem[0].id = newId;

            var text = dataCDataItem[0].childNodes[1].data;
            var amount = byId("amount_" + id).value;
            var price = $("#" + id + "selectedLine .price-col")[0].innerText;
            // $(dataCDataItem).appendTo("#selectedEquipmentCDataField");
            $("#selectedEquipmentCDataField").append($(`

        <div class="row" id ="CData`+ id + `">
            <div class="col CDataMainCol">
                `+ text + `
            </div>             
            <div class="col-sm CDataCol">
                `+ price + `
            </div> 
            <div class="col-sm CDataCol">
                `+ amount + ` шт.
            </div> 

        </div> 
        `));

        })
        if ($("#selectedEquipmentCDataField")[0].childNodes.length < 2) {
            $("#noEquipmentExceptionCDataField").show();
            byId("isAnyEquipmentSelected").value = "";
        }
        else {
            $("#noEquipmentExceptionCDataField").hide();
            byId("isAnyEquipmentSelected").value = "true";
        }
    }

}

function validateData(textIfValid, textIfNotValid) {

}


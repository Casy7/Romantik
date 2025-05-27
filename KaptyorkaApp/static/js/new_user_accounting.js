$("select#demo2").treeMultiselect({ searchable: true, searchParams: ['section', 'text'], onChange: treeOnChange });

var totalPrice = 0;

$(".item").toArray().forEach(countPrice);


function treeOnChange(allSelectedItems, addedItems, removedItems) {

    $(".tree-multiselect .selected .item").toArray().forEach(addPrice);
    updatePrice();
}

$('#userSelector').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
  $('#userId')[0].value = $('#userSelector')[0][clickedIndex].dataset.tokens;
});
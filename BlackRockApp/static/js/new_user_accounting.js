

$('#userSelector').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
  $('#userId')[0].value = $('#userSelector')[0][clickedIndex].dataset.tokens;
});
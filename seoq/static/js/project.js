/* Project specific Javascript goes here. */
$('#question-tabs a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
});
function showLength(id){
  document.getElementById(id+'-span').innerHTML = document.getElementById(id).value.length;
}
    // Code that uses jQuery's $ can follow here.
/* Project specific Javascript goes here. */
// Q&A Scripts
// Character count in New Question fields
function showLength(id){
  document.getElementById(id+'-span').innerHTML = document.getElementById(id).value.length;
}
// Form for answer question
$('form.form-post .reply-input').focus(function() {
	$(this).addClass('active');
	$(this).parent().find('.post').show();
});
// Hide or show replies
$('.hide-replies').click(function () {
  var element = $(this).parent().next();
  var hidden = element.hasClass('in');
  if (hidden) {
    $(this).html('<i class="fa fa-angle-down"></i>Show replies');
  }
  else{
    $(this).html('<i class="fa fa-angle-up"></i>Hide replies');
  }
});
function hideShare(type, id){
	document.getElementById('share-'+type+'-'+id).style.display = 'none';
	document.getElementById('share-media-'+type+'-'+id).style.display = 'block';
}
function showShare(type, id){
	document.getElementById('share-'+type+'-'+id).style.display = 'block';
	document.getElementById('share-media-'+type+'-'+id).style.display = 'none';
}
function showSection(id){
	document.getElementById(id).style.display = 'block';
}
function hideSection(id){
	document.getElementById(id).style.display = 'none';
}
// Function to change answer text for a textarea
$('a[id^="edit-"]').click(function () {
	$(this).parent().parent().find('button').show();
	var txt = $(this).parent().parent().find('div[id^="ans-"]').text();
	$(this).parent().parent().find('div[id^="ans-"]').html('<textarea name="answer_text">'+txt+'</textarea>');
	$(this).hide();
});

window.onload = function() {
  if (document.getElementsByClassName('footer_date')[0] != undefined) {
    const date = new Date().getFullYear()
    document.getElementsByClassName('footer_date')[0].innerHTML = date + ' ';
  }
  document.body.style.visibility = 'visible';
}

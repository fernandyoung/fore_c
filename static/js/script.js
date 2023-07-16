function ButtonClr(){
var btnContainer = document.getElementById("myDiv");

var btn= btnContainer.getElementsByClassName("btn");

for (var i = 0; i < btn.length; i++) {
	btn[i].addEventListener("click",
		function(){
			var current=document.getElementsByClassName("btn-gede_act");
			current[0].className=current[0].className.replace("btn-gede_act","");
			this.className += "btn-gede_act";
		}
		);
}}

function downloadFile(){
	window.location.href='/download';
}

function setAction(action){
	document.getElementById('myForm').action=action;
}

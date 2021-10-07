document.addEventListener("DOMContentLoaded", function () {
  let allEditLinks = document.querySelectorAll(".editLink");

  allEditLinks.forEach((link) => {
    link.onclick = (e) => {
      const postDiv = e.target.parentElement;
      postDiv.style.display = "none";

      const form = document.createElement("form");
      form.onsubmit = function (event) {
        event.preventDefault();

        //https://stackoverflow.com/questions/9713058/send-post-data-using-xmlhttprequest
        const req = new XMLHttpRequest();
        req.open("POST", '/editPost', true);
        const csrftoken = getCookie("csrftoken");

        req.setRequestHeader("X-CSRFToken", csrftoken);

        req.onload = () => {
          form.style.display = "none";
          postDiv.querySelector("#textDiv").innerHTML = editArea.value;
          postDiv.style.display = "block";
          
        };

        data = {
          post_id: postDiv.dataset.post_id,
          newText: editArea.value,
        };

        req.send(JSON.stringify(data));
        
      };

      const innerDiv = document.createElement('div');
      innerDiv.className = "card text-center w-75 card border-light mb-3";
      
      const editArea = document.createElement("textarea");
      editArea.value = postDiv.querySelector("#textDiv").innerHTML;
      editArea.className = "form-control";
      
      const submitButton = document.createElement("input");
      submitButton.type = "submit";
      submitButton.className = "btn btn-primary";
      submitButton.style.marginTop = "15px";
      submitButton.value = "Save Post";

      form.appendChild(editArea);
      form.appendChild(submitButton);
      
      innerDiv.appendChild(form);

      postDiv.parentNode.appendChild(innerDiv);

      e.preventDefault();
    };
  });
  
});

//https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

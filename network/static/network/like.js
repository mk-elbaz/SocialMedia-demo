document.addEventListener("DOMContentLoaded", function () {
    let allLikeLinks = document.querySelectorAll(".like-link");

    allLikeLinks.forEach(link => {
        link.onclick = (e) => {
            const postDiv = e.target.parentElement.parentElement;
            try {
                var likeAuthor = document.querySelector("#loggedusername").innerHTML;
            } catch (TypeError) {
                alert("You must login first!");
                return false;
            }
            postID = postDiv.dataset.post_id;
            const data = {
                post_id : postDiv.dataset.post_id,
                likeAuthor : likeAuthor
            }
            fetch('/changeLike',{
                method : 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            }).then(res => res.json())
            .then(data => {
                e.target.innerHTML = data.likesCount
                if(data.like){
                    e.target.classList.remove('far')
                    e.target.classList.add('fas')
                }else{
                    e.target.classList.remove('fas')
                    e.target.classList.add('far')
                }
            }).catch(error => console.error(error));
        }
    })

});


//https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  
document.getElementById("postForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    title: document.getElementById("title").value || null,
    content: document.getElementById("content").value,
    school_id: parseInt(document.getElementById("school_id").value)
  };

  const res = await fetch("/posts/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const msg = document.getElementById("message");

  if (res.ok) {
    msg.innerText = "Post publicado";
    document.getElementById("postForm").reset();
  } else {
    msg.innerText = "Error al publicar";
  }
});

console.log("post.js cargado");

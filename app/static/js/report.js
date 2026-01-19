async function reportPost(postId) {
  if (!confirm("¿Reportar esta publicación?")) return;

  const res = await fetch(`/posts/${postId}/report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      reason: "general"
    })
  });

  if (res.ok) {
    alert("Publicación reportada. Gracias.");
  } else if (res.status === 400) {
    alert("Ya reportaste esta publicación.");
  } else {
    alert("Error al reportar.");
  }
}

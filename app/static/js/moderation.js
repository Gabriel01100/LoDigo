async function hidePost(postId) {
  if (!confirm("¿Ocultar este post?")) return;

  const res = await fetch(`/posts/${postId}/hide`, {
    method: "PATCH"
  });

  if (res.ok) {
    alert("Post ocultado");
    location.reload();
  } else {
    alert("Error al ocultar");
  }
}

async function restorePost(postId) {
  if (!confirm("¿Restaurar este post?")) return;

  const res = await fetch(`/posts/${postId}/restore`, {
    method: "PATCH"
  });

  if (res.ok) {
    alert("Post restaurado");
    location.reload();
  } else {
    alert("Error al restaurar");
  }
}

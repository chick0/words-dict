function fetchData(wordId) {
    try {
        console.log(Swal)
    } catch {
        setTimeout(() => {
            fetchData(wordId)
        }, 100)

        return
    }

    Swal.fire({
        text: "단어 정보를 불러오고 있습니다.",
        icon: "info",
        showConfirmButton: false,
        allowEscapeKey: false,
        allowOutsideClick: false,
    })

    fetch(`/word/raw?id=${wordId}`)
        .then((resp) => resp.json())
        .then((json) => {
            if (json.status == true) {
                Swal.close()

                document.getElementById("word").value = json.payload.word
                document.querySelector("select").value = json.payload.category ?? 'x'
                tinymce.activeEditor.setContent(json.payload.meaning)
            } else {
                Swal.fire({
                    html: json.message,
                    icon: "error",
                    confirmButtonText: "확인",
                    timer: 5000,
                    timerProgressBar: true,
                }).then(() => {
                    history.back()
                })
            }
        })
        .catch(() => {
            Swal.fire({
                html: `단어 정보를 불러오는 과정에서 문제가 발생하였습니다<br>해당 문제가 반복해서 발생한다면 담당자한테 문의해주세요.`,
                icon: "error",
                confirmButtonText: "확인",
                timer: 5000,
                timerProgressBar: true,
            }).then(() => {
                history.back()
            })
        })
}

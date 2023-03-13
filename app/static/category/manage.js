function categorySelectForManageTool(categoryId) {
    selectedCategory = categoryId
    document.getElementById("category-detail").classList.add("visually-hidden")
    loadSelectOption()
}

function loadSelectOption() {
    const parent = document.getElementById("parent")
    parent.innerHTML = ""

    fetch("/category")
        .then((resp) => resp.json())
        .then((json) => {
            const noParent = document.createElement("option")
            noParent.value = -1
            noParent.text = "상위 카테고리 없음"

            parent.appendChild(noParent)

            json.forEach((category) => {
                const option = document.createElement("option")
                option.value = category.id
                option.text = category.text

                parent.appendChild(option)
            })

            if (selectedCategory == "new") {
                document.querySelector("#text").value = ""
                document.querySelector("select").value = -1

                // Finished!
                document.getElementById("category-detail").classList.remove("visually-hidden")
            } else {
                loadOption()
            }
        })
}

function loadOption() {
    fetch(`/category/${selectedCategory}/detail`)
        .then((resp) => resp.json())
        .then((json) => {
            document.querySelector("#text").value = json.text

            let parent = json.parent

            if (parent == null) {
                parent = -1
            }

            document.querySelector("select").value = parent

            // Finished!
            document.getElementById("category-detail").classList.remove("visually-hidden")
        })
}

let selectedCategory = ""

window.categoryManage = true

document.querySelector("select").addEventListener("change", () => {
    let select = document.querySelector("select")
    let eventSelected = Number(select.value)

    if (eventSelected === selectedCategory) {
        Swal.fire({
            html: "자기 자신을 상위 카테고리로 설정 할 수 없습니다.<br>다른 카테고리를 선택해주세요.",
            icon: "error",
            confirmButtonText: "확인",
            timer: 5000,
            timerProgressBar: true,
        })

        select.value = ""
        return
    }

    fetch(`/category/${eventSelected}/parent-able`)
        .then((resp) => resp.json())
        .then((json) => {
            if (json.result == false) {
                Swal.fire({
                    html: "해당 카테고리는 상위 카테고리로 설정할 수 없습니다.<br>다른 카테고리를 선택해주세요.",
                    icon: "error",
                    confirmButtonText: "확인",
                    timer: 5000,
                    timerProgressBar: true,
                })

                select.value = ""
            } else if (json.result == null) {
                Swal.fire({
                    text: "선택한 카테고리는 등록된 카테고리가 아닙니다.",
                    icon: "error",
                    confirmButtonText: "확인",
                    timer: 5000,
                    timerProgressBar: true,
                })

                select.value = ""
            }
        })
})

document.getElementById("save").addEventListener("click", () => {
    if (selectedCategory == "") {
        Swal.fire({
            text: "카테고리를 선택하고 저장 버튼을 클릭해주세요.",
            icon: "error",
            confirmButtonText: "확인",
            timer: 5000,
            timerProgressBar: true,
        })

        return
    }

    fetch("/category/control", {
        method: "POST",
        headers: {
            "Content-Type": `application/json`,
        },
        body: JSON.stringify({
            id: selectedCategory,
            text: document.querySelector("#text").value,
            parent: document.querySelector("select").value,
        }),
    })
        .then((resp) => resp.json())
        .then((json) => {
            if (json.status === true) {
                location.reload()
            } else {
                Swal.fire({
                    html: json.message,
                    icon: "error",
                    confirmButtonText: "확인",
                    timer: 5000,
                    timerProgressBar: true,
                })
            }
        })
})

document.getElementById("new").addEventListener("click", () => {
    selectedCategory = "new"
    loadSelectOption()
})

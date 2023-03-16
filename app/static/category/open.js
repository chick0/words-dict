function searchCategory(id) {
    if (id == null) {
        console.warn("해당 단어는 선택된 카테고리가 없습니다.")
        return
    }

    const elementId = `category-${id}`
    let element = document.getElementById(elementId)

    let tryToGetElement = setInterval(() => {
        if (element == null) {
            console.warn(
                "카테고리을 버튼 찾을 수 없습니다... 카테고리 정보를 로딩하는 과정이 끝나지 않았을 가능성이 높습니다. 잠시뒤에도 해당 메시지가 반복적으로 나온다면 담당자한테 연락해주세요."
            )
            element = document.getElementById(elementId)
        } else {
            clearInterval(tryToGetElement)
            openCategory(element)
        }
    }, 100)
}

function openCategory(element) {
    function openCollapse(target) {
        target.parentNode.querySelector("button").setAttribute("aria-expanded", "true")
        target.classList.add("show")
    }

    const parent = document.getElementById(element.dataset.parentId)

    if (parent == null) {
        openCollapse(element)
    } else {
        openCollapse(parent)
        element.classList.add("is-focused")
    }
}

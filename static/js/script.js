document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".view-image-btn");
    const imageContainer = document.getElementById("image-container");
    const cardImage = document.getElementById("card-image");

    buttons.forEach(button => {
        button.addEventListener("click", async () => {
            const cardId = button.getAttribute("data-id");
            const extension = new URLSearchParams(window.location.search).get("extension");
            
            try {
                const response = await fetch("/image_url", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ card_id: cardId, extension: extension })
                });
                const data = await response.json();
                cardImage.src = data.image_url;
                cardImage.style.display = "block";
            } catch (error) {
                console.error("Error fetching image:", error);
            }
        });
    });
});

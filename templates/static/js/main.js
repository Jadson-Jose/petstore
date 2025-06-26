// Função para adicionar ao carrinho
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar ao carrinho
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const cartCount = document.querySelector('.cart-count');
            
            // Simular requisição AJAX
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({quantity: 1})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    cartCount.textContent = data.cart_count;
                    
                    // Feedback visual
                    this.style.backgroundColor = '#2ecc71';
                    setTimeout(() => {
                        this.style.backgroundColor = '#4CAF50';
                    }, 500);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Função para obter o cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
window.addEventListener('DOMContentLoaded', () => {
    const agreeCheckbox = document.getElementById('agree');
    const submitBtn = document.getElementById('submit');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    // 選取錯誤訊息的span
    const emailError = emailInput.parentElement.querySelector('span');
    const passwordError = passwordInput.parentElement.querySelector('span');


    // 監聽change事件，在輸入完成時檢查信箱格式
    emailInput.addEventListener('change', (e) => {
        // 格式不正確
        if (e.target.value && !e.target.validity.valid) {
            emailError.classList.remove('hidden');
            emailInput.classList.add('border-red-500', 'text-red-600');
            emailInput.classList.remove('border-gray-300');
        }
        else {
            emailError.classList.add('hidden');
            emailInput.classList.remove('border-red-500', 'text-red-600');
            emailInput.classList.add('border-gray-300');
        }
    });

    // 監聽change事件，在輸入完成時檢查密碼格式
    passwordInput.addEventListener('change', (e) => {
        // 沒有要求的密碼格式，只檢查是否有輸入
        if (e.target.value.length === 0) {
            passwordError.classList.remove('hidden');
            passwordInput.classList.add('border-red-500', 'text-red-600');
            passwordInput.classList.remove('border-gray-300');
        } else {
            passwordError.classList.add('hidden');
            passwordInput.classList.remove('border-red-500', 'text-red-600');
            passwordInput.classList.add('border-gray-300');
        }
    });

    // 監聽submit點擊事件，若沒有勾選同意則跳出alert
    submitBtn.addEventListener('click', (e) => {
        if (!agreeCheckbox.checked) {
            e.preventDefault();
            alert('請勾選同意條款');
        } else {
            return true;
        }
    });
});
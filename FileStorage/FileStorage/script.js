const username = document.querySelector('#username')
const password = document.querySelector('#password')
const cpassword = document.querySelector('#c-password')
const email = document.querySelector('#email')
const emailErr = document.querySelector('.email')
const usernameErr = document.querySelector('.username')
const passwordErr = document.querySelector('.password')
const passErr = document.querySelector('.password-error')
const cPassErr = document.querySelector('.c-password')
const hide = document.querySelectorAll('.hide')
const SignIn = document.querySelector('#SignIn')
const Login = document.querySelector('#Login')
const emailUser = document.querySelector('#emailUser')
const card1 = document.querySelector('#card1')


const fileModal1 = document.querySelector('#file1')
const fileModal2 = document.querySelector('#file2')
const openModal = document.querySelectorAll('.openModal')


const emailPattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
const englishPattern = /\b\w*a\w*\b/;

if (emailUser?.value === '' || password?.value === '') {
    if (Login) {
        Login.disabled = true
    }
}

card1.addEventListener('click', (e) => {
    e.target.parentElement.classList.toggle('relative')
    fileModal1.classList.toggle('hidden')
})


// openModal?.forEach(elem => {
//     elem.addEventListener('click', (e) => {
//         // console.log(e.target);
//         e.target.parentElement.classList.toggle('relative')
//         fileModal1.classList.toggle('hidden')
//     })
// })


function charCount(e, c) {
    const count = e.target.value
    if (count.length <= c) {
        // e.target.nextElementSibling.nextElementSibling.textContent = `It must be ${c} characters!`
        e.target.classList.add('border')
        e.target.classList.add('border-red-400')
        if (SignIn) {
            SignIn.disabled = true
        }
        return false
    } else {
        // e.target.nextElementSibling.nextElementSibling.textContent = ``
        e.target.classList.remove('border')
        e.target.classList.remove('border-red-400')
        if (SignIn) {
            SignIn.disabled = false
        }
        return true
    }

}
function validateEmail(email) {
    return emailPattern.test(email);
}
function validateEnglish(letter) {
    return englishPattern.test(letter);
}
const errorElements = document.querySelectorAll('.error');

password?.addEventListener('keyup', (e) => {
    if (!charCount(e, 6)) {
        if (passwordErr) {
            passwordErr.textContent = 'It must be 6 characters'
        } else if (passErr) {
            passErr.textContent = 'It must be 6 characters'
        }
    } else {
        if (passwordErr) {
            passwordErr.textContent = ''
        } else if (passErr) {
            passErr.textContent = ''
        }
    }

    if (Login) Login.disabled = false
})

hide.forEach((el) => {
    el.addEventListener('click', (e) => {
        if (e.target.previousElementSibling.type == 'password')
            e.target.previousElementSibling.type = 'text'
        else
            e.target.previousElementSibling.type = 'password'
    })
})

username?.addEventListener('keyup', (e) => {
    if (!validateEnglish(e.target.value)) {
        usernameErr.textContent = 'Please type english letters!!!'
        e.target.classList.add('border', 'border-red-400');
        SignIn.disabled = true
    } else if (!charCount(e, 4)) {
        usernameErr.textContent = 'It must be 4 characters!'
        SignIn.disabled = true

    } else {
        usernameErr.textContent = ''
        e.target.classList.remove('border', 'border-red-400');
        SignIn.disabled = false
    }
})


cpassword?.addEventListener('keyup', (e) => {
    if (password.value !== e.target.value) {
        cPassErr.textContent = 'confirm password is incorrect'
        e.target.classList.add('border')
        SignIn.disabled = true
        e.target.classList.add('border-red-400')
    } else {
        cPassErr.textContent = ''
        e.target.classList.remove('border')
        e.target.classList.remove('border-red-400')
        SignIn.disabled = false
    }

})

email?.addEventListener('keyup', (e) => {
    if (!validateEmail(e.target.value)) {
        emailErr.textContent = 'Email is not valid'
        e.target.classList.add('border')
        SignIn.disabled = true
        e.target.classList.add('border-red-400')
    } else {
        emailErr.textContent = ''
        e.target.classList.remove('border')
        e.target.classList.remove('border-red-400')
        SignIn.disabled = false
    }
})


if (email?.value === '' || username?.value === '' || password?.value === '' || cpassword?.value === '') {
    if (SignIn) {
        SignIn.disabled = true
    }
}

// if (SignIn.disabled === true) {
//     SignIn.classList.add('opacity-50')
//     SignIn.classList.add('cursor-not-allowed')
// }


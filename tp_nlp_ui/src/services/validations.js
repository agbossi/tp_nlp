const simpleIsPresent = (value) => {
    let is = true
    if(!value) {
        is = false
    }
    return is
}

const messageIsPresent = (value, errors, message="Campo obligatorio") => {
    let is = true
    if(!value) {
        is = false
        errors.push(message)
    }
    return is
}

const checkPresent = (values) => {
    let arePresent = true
    values.forEach(value => arePresent &&= simpleIsPresent(value))
    return arePresent
}

const checkDecimal = (value, errors, message) => {
    let isDecimal = true
    if(!/^-?\d+(\.\d{1,3})?$/.test(value)) {
        isDecimal = false
        errors.push(message)
    }
    return isDecimal
}

const requiredDecimal = (value, errors) => {
    return !messageIsPresent(value, errors, "Campo obligatorio")
        || !checkDecimal(value, errors, "No es numero decimal")
}

export default {
    checkPresent,
    requiredDecimal,
    messageIsPresent
}
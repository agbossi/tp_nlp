import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import {Button, Col, Container, DropdownButton, Row} from "react-bootstrap";
import Dropdown from 'react-bootstrap/Dropdown';
import {useEffect, useState} from "react";
import '../../services/validations'
import validations from "../../services/validations";
import apiCalls from "../../services/api/apiCalls";
import ErrorMessage from "../ErrorMessage";
import {Link} from "react-router-dom";

function PlaceForm() {
    const [lugar, setLugar] = useState("")
    const [latitud, setLatitud] = useState(0.0)
    const [longitud, setLongitud] = useState(0.0)
    const [lugares, setLugares] = useState([])
    const [lugarElegido, setLugarElegido] = useState(null)
    const [erroresLugar, setErroresLugar] = useState([])
    const [erroresLat, setErroresLat] = useState([])
    const [erroresLng, setErroresLng] = useState([])
    const [invalidForm, setInvalidForm] = useState(true)
    const [message, setMessage] = useState("")

    const onSubmit = async (e) => {
        e.preventDefault()
        setInvalidForm(true)
        if(validations.checkPresent([lugar, latitud, longitud])) {
            let data = {
                "name": lugar, "latitude": latitud, "longitude": longitud
            }
            await apiCalls.createPlace(data).then(response => {
                if(response.status === 201) {
                    setLugares([...lugarElegido, response.data])
                    setMessage('Lugar creado, ya disponible en lista')
                } else {
                    setMessage(response.data)
                }
            }).catch(error => {
                setMessage(error.message)
            })
        } else {
            setMessage('Complete todos los datos')
        }
    }

    const onChange = (event) => {
        let error = false
        let errors = []
        // eslint-disable-next-line default-case
        switch (event.target.id) {
            case "formLugar":
                setLugar(event.target.value)
                error ||= !validations.messageIsPresent(event.target.value, errors)
                setErroresLugar(errors)
                break
            case "formLat":
                setLatitud(event.target.value)
                error ||= validations.requiredDecimal(event.target.value, errors)
                setErroresLat(errors)
                break
            case "formLng":
                setLongitud(event.target.value)
                error ||= validations.requiredDecimal(event.target.value, errors)
                setErroresLng(errors)
                break
        }
        setInvalidForm(error)
    }

    const handleSelect = (lugar) => {
        setLugarElegido(lugar)
    }

    const fetchPlaces = async () => {
        const response = await apiCalls.getPlaces()
        if(response.status === 200)
            setLugares(response.data)
    }

    const dropdownTitle = (elem) => {
        if(elem === null)
            return 'Seleccione lugar'
        return elem.name
    }

    useEffect( () => {
        fetchPlaces()
    }, [])

    return (
        <>
            <Container>
                <Row>
                    <Col>
                        <Form.Group className="mb-3" id="selectLugar">
                            <Form.Label>Lugares</Form.Label>
                            <DropdownButton id="dropdown-lugares-button" title={dropdownTitle(lugarElegido)}>
                                <Dropdown.Item id={'ddlNone'}
                                               onClick={() => setLugarElegido(null)}>
                                    -
                                </Dropdown.Item>
                                {lugares.map((lugar, index) => {
                                    if(lugar === lugarElegido) {
                                        return <Dropdown.Item
                                            id={'ddl' + index}
                                            eventKey={lugar} active
                                            onClick={() => {
                                                handleSelect(lugar)
                                            }}>
                                            {lugar.name}
                                        </Dropdown.Item>
                                    } else {
                                        return <Dropdown.Item eventKey={lugar}
                                                              onClick={() => {handleSelect(lugar)}}>
                                            {lugar.name}
                                        </Dropdown.Item>
                                    }
                                })}
                            </DropdownButton>
                        </Form.Group>
                        {lugarElegido !== null && <Button variant="outline-primary" size="lg">
                                <Link to={"results/" + lugarElegido.placeId}>
                                    Ver
                                </Link>
                            </Button>}
                    </Col>
                    <Col>
                        <Form onSubmit={onSubmit}>
                            <Form.Group className="mb-3">
                                <Form.Label>Lugar</Form.Label>
                                <Form.Control type="text"
                                              id="formLugar"
                                              placeholder="Ingrese nombre lugar"
                                              onChange={onChange} />
                                <Form.Text className="text-muted">
                                    Tal como aparece en maps.
                                </Form.Text>
                            </Form.Group>
                            {erroresLugar.length > 0 && invalidForm && <ErrorMessage id="lugarErrors" errors={erroresLugar}/>}
                            <Form.Label>Coordenadas</Form.Label>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>@</InputGroup.Text>
                                    <Form.Control aria-label="Latitud"
                                                  placeholder="Ingrese latitud"
                                                  id="formLat"
                                                  onChange={onChange} />
                                <InputGroup.Text>,</InputGroup.Text>
                                <Form.Control aria-label="Longitud"
                                              placeholder="Ingrese longitud"
                                              id="formLng"
                                              onChange={onChange}/>
                            </InputGroup>
                            <Form.Text className="text-muted">
                                Sugerencia: use la url de maps.
                            </Form.Text>
                            {erroresLugar.length > 0 && invalidForm && <ErrorMessage id="lugarErrors" errors={erroresLat}/>}
                            {erroresLugar.length > 0 && invalidForm && <ErrorMessage id="lugarErrors" errors={erroresLng}/>}
                            <br/>
                            <br/>
                            <Button variant="primary" disabled={invalidForm && latitud !== 0.0 && longitud !== 0.0}
                                    type="submit">
                                Agregar
                            </Button>
                        </Form>
                        {message && (
                            <div className="form-group">
                                <div className="alert alert-danger m-3" role="alert">
                                    {message}
                                </div>
                            </div>
                        )}
                    </Col>
                </Row>
            </Container>
        </>
    )
}

export default PlaceForm;
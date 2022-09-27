import {Button, Form, Modal} from "react-bootstrap";
import {useState} from "react";

function AddWordModal(props) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [word, setWord] = useState("")

    const handleAdd = () => {
        if(word !== undefined && word !== "")
            props.handleAdd(word)
        handleClose()
    }

    const onChange = (event) => {
        setWord(event.target.value)
    }

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Agregar palabra
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Nueva palabra a la blacklist</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <Form.Label>Nueva palabra</Form.Label>
                            <Form.Control
                                type="email"
                                value={word}
                                placeholder="Palabra"
                                onChange={onChange}
                                autoFocus
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Cerrar
                    </Button>
                    <Button variant="primary" onClick={handleAdd}>
                        Agregar
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
} export default AddWordModal;
import Button from 'react-bootstrap/Button';

function UpdateButtonBlock(props) {
    return (
        <div className="d-grid gap-2">
            <Button variant="primary" size="lg" onClick={props.update}>
                Agregar reviews
            </Button>
            <Button variant="secondary" size="lg" onClick={props.recompute}>
                Recomputar
            </Button>
        </div>
    );
}

export default UpdateButtonBlock;
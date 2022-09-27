function ErrorMessage(props) {
    return (
        <>
            <div className="form-group">
                <div className="alert alert-danger" role="alert">
                    <ul id={props.id}>
                        {props.errors.map((error, index) => {
                            return (
                                <li key={index}>{error}</li>
                            )
                        })}
                    </ul>
                </div>
            </div>
        </>
    )
}

export default ErrorMessage;
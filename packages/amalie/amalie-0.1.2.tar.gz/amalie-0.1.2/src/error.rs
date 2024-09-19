
#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("Invalid input because {0}")]
    InvalidInput(String),

    #[error("Invalid State because {0}")]
    InvalidState(String),

    #[error("The function did not find any result")]
    NoResult,

    #[error("Inverse does not exist")]
    InverseNotExist,

    #[error("Unable to convert value")]
    CouldNotConvert,

    #[error("Unable to parse value")]
    CouldNotParse,

    #[error("Feature is not supported")]
    NotSupported,
}

pub type Result<T> = core::result::Result<T, Error>;

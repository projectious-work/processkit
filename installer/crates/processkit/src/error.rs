//! Internal installer errors with a compatibility-preserving wire adapter.

use serde::Serialize;
use std::fmt;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum InstallerErrorKind {
    RequestRead,
    RequestDecode,
    RequestValidation,
    ReleaseVerification,
    Operation,
    Serialization,
    Legacy,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum ExitClass {
    General,
}

impl ExitClass {
    pub(crate) const fn code(self) -> i32 {
        match self {
            Self::General => 3,
        }
    }
}

#[derive(Debug)]
pub(crate) struct InstallerError {
    kind: InstallerErrorKind,
    message: String,
    path: String,
    exit: ExitClass,
}

#[derive(Serialize)]
pub(crate) struct RequestProblem<'a> {
    code: &'static str,
    path: &'a str,
    message: &'a str,
}

impl InstallerError {
    fn new(kind: InstallerErrorKind, message: String) -> Self {
        Self {
            kind,
            message,
            path: String::new(),
            exit: ExitClass::General,
        }
    }

    pub(crate) fn request_read(message: String) -> Self {
        Self::new(InstallerErrorKind::RequestRead, message)
    }

    pub(crate) fn request_decode(message: String) -> Self {
        Self::new(InstallerErrorKind::RequestDecode, message)
    }

    pub(crate) fn request_validation(message: String) -> Self {
        Self::new(InstallerErrorKind::RequestValidation, message)
    }

    pub(crate) fn release_verification(message: String) -> Self {
        Self::new(InstallerErrorKind::ReleaseVerification, message)
    }

    pub(crate) fn operation(message: String) -> Self {
        Self::new(InstallerErrorKind::Operation, message)
    }

    pub(crate) fn serialization(message: String) -> Self {
        Self::new(InstallerErrorKind::Serialization, message)
    }

    pub(crate) fn request_problem(&self) -> RequestProblem<'_> {
        let _ = self.kind;
        RequestProblem {
            code: "request-failed",
            path: &self.path,
            message: &self.message,
        }
    }

    pub(crate) const fn exit_code(&self) -> i32 {
        self.exit.code()
    }
}

impl fmt::Display for InstallerError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl From<String> for InstallerError {
    fn from(message: String) -> Self {
        Self::new(InstallerErrorKind::Legacy, message)
    }
}

impl From<&str> for InstallerError {
    fn from(message: &str) -> Self {
        Self::from(message.to_owned())
    }
}

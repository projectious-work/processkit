//! Stable JSON rendering for the human CLI and machine protocol.

use crate::error::InstallerError;
use serde::Serialize;

pub(crate) fn pretty_json<T: Serialize>(value: &T) -> Result<String, InstallerError> {
    serde_json::to_string_pretty(value)
        .map_err(|error| InstallerError::serialization(error.to_string()))
}

#[cfg(test)]
mod tests {
    use super::pretty_json;
    use serde::ser::{Error, Serializer};
    use serde::Serialize;

    struct FailingValue;

    impl Serialize for FailingValue {
        fn serialize<S>(&self, _serializer: S) -> Result<S::Ok, S::Error>
        where
            S: Serializer,
        {
            Err(S::Error::custom("fixture serialization failure"))
        }
    }

    #[test]
    fn serialization_failure_is_typed_instead_of_panicking() {
        let error = pretty_json(&FailingValue).expect_err("must fail");
        assert_eq!(error.to_string(), "fixture serialization failure");
        assert_eq!(error.exit_code(), 3);
    }
}

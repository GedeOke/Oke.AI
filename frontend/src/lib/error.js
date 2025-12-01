export const getErrorMessage = (err) => {
  let msg = "";
  let code = "";
  if (err?.response?.data) {
    if (typeof err.response.data === "string") msg = err.response.data;
    else {
      code = err.response.data.code || err.response.data.error_code || "";
      msg =
        err.response.data.message ||
        err.response.data.detail ||
        err.response.data.error ||
        JSON.stringify(err.response.data);
    }
  } else if (err?.message) {
    msg = err.message;
  }

  if (code === "invalid_credentials") {
    return "Email atau password salah.";
  }

  if (/status code/i.test(msg)) {
    return "Terjadi kesalahan. Cek kredensial atau server.";
  }
  return msg || "Terjadi kesalahan. Silakan coba lagi.";
};

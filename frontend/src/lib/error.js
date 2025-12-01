export const getErrorMessage = (err) => {
  if (err?.response?.data) {
    if (typeof err.response.data === "string") return err.response.data;
    return (
      err.response.data.message ||
      err.response.data.detail ||
      err.response.data.error ||
      JSON.stringify(err.response.data)
    );
  }
  if (err?.message) return err.message;
  return "Terjadi kesalahan. Silakan coba lagi.";
};

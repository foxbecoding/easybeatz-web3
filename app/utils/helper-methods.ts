export function isEmpty(value: any) {
  return (
    value === undefined ||
    value === null ||
    value === "" ||
    (Array.isArray(value) && value.length === 0) ||
    (typeof value === "object" && value !== null && Object.keys(value).length === 0)
  );
}

export const numbersOnlyInput = (event: any) => {
  const invalidChars = ['+', '-', '.'];

  if (invalidChars.includes(event.key)) {
    event.preventDefault(); // Block '+' and '-' from being entered
    return;
  }

  let value = event.target.value;

  // Remove non-digit characters (just in case)
  value = value.replace(/\D/g, '');

  // Remove leading zeros
  value = value.replace(/^0+/, '');
};


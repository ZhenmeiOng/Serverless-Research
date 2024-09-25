'use strict'
const PDFDocument = require('pdfkit')

module.exports = async (event, context) => {
  const payment = 100;

  let pdf = await createBrotliDecompress(payment)
  return context
    .status(200)
    .headers({
      "Content-type": "application/pdf"
    })
    .succeed(pdf)
}

function createDocument() {
  return new Promise(resolve=> {
    const doc = new PDFDocument({
      size: "LEGAL",
      title: "OpenFaas Invoice",
      author: "OpenFaas Ltd"
    });

    const buffers = [];
    doc.on("data", buffers.push.bind(buffers));
    doc.on("end", () => {
      resolve(Buffer.concat(buffers));
    })

    let PAYMENT = 100;
    doc.text(`Invoice amount: ${PAYMENT}USD`);
    doc.end();
  });
}
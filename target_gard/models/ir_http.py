from odoo import api ,models, fields,_


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'


    def binary_content(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       unique=False, filename=None, filename_field='name', download=False,
                       mimetype=None, default_mimetype='application/octet-stream',
                       access_token=None):
        dict1 = {

        }
        dict1 [xmlid] = xmlid
        dict1 [model] = model
        dict1 [id] = id
        dict1 [field] = field
        dict1 [unique] = unique
        dict1 [filename] = filename
        dict1 [filename_field] = filename_field
        dict1 [download] = download
        dict1 [mimetype] = mimetype
        dict1 [default_mimetype] = default_mimetype
        dict1 [access_token] = access_token
        """ Get file, attachment or downloadable content

        If the ``xmlid`` and ``id`` parameter is omitted, fetches the default value for the
        binary field (via ``default_get``), otherwise fetches the field for
        that precise record.

        :param str xmlid: xmlid of the record
        :param str model: name of the model to fetch the binary from
        :param int id: id of the record from which to fetch the binary
        :param str field: binary field
        :param bool unique: add a max-age for the cache control
        :param str filename: choose a filename
        :param str filename_field: if not create an filename with model-id-field
        :param bool download: apply headers to download the file
        :param str mimetype: mintype of the field (for headers)
        :param str default_mimetype: default mintype if no mintype found
        :param str access_token: optional token for unauthenticated access
                                 only available  for ir.attachment
        :returns: (status, headers, content)
        """
        record, status = super(IrHttp,self).sudo()._get_record_and_check(xmlid=xmlid, model=model, id=id, field=field, access_token=access_token)
        if not record:
            return (status or 404, [], None)

        content, headers, status = None, [], None

        if record._name == 'ir.attachment':
            status, content, filename, mimetype, filehash = super(IrHttp,self)._binary_ir_attachment_redirect_content(record, default_mimetype=default_mimetype)
        if not content:
            status, content, filename, mimetype, filehash = super(IrHttp,self)._binary_record_content(
                record, field=field, filename=filename, filename_field=filename_field,
                default_mimetype='application/octet-stream')

        status, headers, content = super(IrHttp,self)._binary_set_headers(
            status, content, filename, mimetype, unique, filehash=filehash, download=download)

        return status, headers, content

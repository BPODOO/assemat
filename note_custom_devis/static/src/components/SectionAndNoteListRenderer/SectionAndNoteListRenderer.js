/** @odoo-module **/

import { registry } from "@web/core/registry";

import { makeContext } from "@web/core/context";
import { ListRenderer } from "@web/views/list/list_renderer";

import { SectionAndNoteListRenderer } from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import { patch } from "@web/core/utils/patch";
import core from 'web.core';

import { StaticList } from "@web/views/basic_relational_model";

import { useAddInlineRecord } from "@web/views/fields/relational_utils";
import { useService } from "@web/core/utils/hooks";

const { Component, useEffect, useEnv, useComponent } = owl;

patch(SectionAndNoteListRenderer.prototype, "note_custom_sale", {
 // Define the patched method here
    setup() {
        this._super.apply(this, arguments);
        this.actionService = useService("action"); //-> Permet de setup le hook d'action
        this.orm = useService('orm');
     },

     // Define a new method
    async _onClickCustomNote(record) {
        const SaleOrder = this.props.list.model.root;
        const resModel = this.props.list.model.root.resModel
        let recordUpdate;
        if ("id" in record.data) {
            await record.update({ 
                name: record.data.name,
            })
            recordUpdate = record
        } else {
            await record.update({ 
                name: " ", 
            })
            await SaleOrder.save({ stayInEdition: true })
            recordUpdate = SaleOrder.data.order_line.records.slice(-1)[0]
        }
        const action = await this.orm.call(record.resModel, 'action_show_details', [recordUpdate.data.id]);
        this.actionService.doAction(action, {
            onClose: async () => {
                await recordUpdate.load();
                await recordUpdate.save({ stayInEdition: true })
            },
        });
     },
    
    isNote(record) {
        const model_load = this.props.list.model.root.resModel
        return record.data.display_type === 'line_note' && model_load == 'sale.order';
    }
    
});

SectionAndNoteListRenderer.recordRowTemplate = "note_custom_devis.SectionListRenderer.RecordRow";
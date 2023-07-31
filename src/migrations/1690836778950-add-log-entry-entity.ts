import { MigrationInterface, QueryRunner } from "typeorm";

export class AddLogEntryEntity1690836778950 implements MigrationInterface {
    name = 'AddLogEntryEntity1690836778950'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "log_entry" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "description" character varying NOT NULL, CONSTRAINT "PK_45e2f8fa5e70dd60266d2f94d49" PRIMARY KEY ("id"))`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP TABLE "log_entry"`);
    }

}

import { MigrationInterface, QueryRunner } from "typeorm";

export class AddClient1716812452217 implements MigrationInterface {
    name = 'AddClient1716812452217'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "client" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "secret" character varying NOT NULL, "productId" uuid, CONSTRAINT "PK_96da49381769303a6515a8785c7" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`DROP TABLE "client"`);
    }

}

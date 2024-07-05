import { MigrationInterface, QueryRunner } from "typeorm";

export class AddUniqueOnProductInClient1716813283611 implements MigrationInterface {
    name = 'AddUniqueOnProductInClient1716813283611'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "UQ_bb082f45ad9dac1c44ac7276357" UNIQUE ("productId")`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "UQ_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

}

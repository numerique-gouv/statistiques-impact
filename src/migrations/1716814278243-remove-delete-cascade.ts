import { MigrationInterface, QueryRunner } from "typeorm";

export class RemoveDeleteCascade1716814278243 implements MigrationInterface {
    name = 'RemoveDeleteCascade1716814278243'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

}
